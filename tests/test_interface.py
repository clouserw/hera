import unittest
import urllib
from urlparse import urlparse

import settings
from interface import Zeus


class TestInterface(unittest.TestCase):

    def setUp(self):
        if len(settings.TEST_URLS) < 2:
            self.fail("Please add at least 2 URLs we can test.")
        self.zeus = Zeus()

    def _loadTestURLs(self):
        for url in settings.TEST_URLS:
            urllib.urlopen(url)

    def test_flushAll(self):
        self._loadTestURLs()

        x = self.zeus.getObjectsByPattern('*')

        # If this is a used box, there is the potential that there are URLs
        # besides the ones we load, so just make sure there are at least that
        # many
        assert len(self.zeus.getObjectsByPattern('*')) >= len(settings.TEST_URLS)

        self.zeus.flushAll()

        assert self.zeus.getObjectsByPattern('*') == None

    def test_flushObjectByPattern(self):
        self._loadTestURLs()
        r = self.zeus.getObjectByPattern(settings.TEST_URLS[0])
        assert len(r) == 1
        self.zeus.flushObjectsByPattern(settings.TEST_URLS[0])
        r = self.zeus.getObjectByPattern(settings.TEST_URLS[0])
        assert r is None

        # Verify a list of flushed URLs is returned
        self._loadTestURLs()
        r = self.zeus.getObjectByPattern(settings.TEST_URLS[0])
        assert len(r) == 1
        f = self.zeus.flushObjectsByPattern(settings.TEST_URLS[0], True)
        assert len(f) == 1
        r = self.zeus.getObjectByPattern(settings.TEST_URLS[0])
        assert r is None

    def test_getObjectByPattern(self):
        self._loadTestURLs()
        r = self.zeus.getObjectByPattern(settings.TEST_URLS[0])
        o = urlparse(settings.TEST_URLS[0])

        assert len(r) == 1
        assert r[0].host == o.netloc
        assert r[0].path == o.path

    def test_getObjectsByPattern(self):
        self.zeus.flushAll()
        self._loadTestURLs()
        r = self.zeus.getObjectsByPattern('*')

        assert len(r) == len(settings.TEST_URLS)
