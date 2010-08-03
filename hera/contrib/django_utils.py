# Just a couple of helpful functions if you're using django.
import logging

from django.conf import settings

from hera import Hera

log = logging.getLogger('z.hera')

def get_hera():
    """Return a Hera object or False on failure."""
    try:
        username = settings.HERA['USERNAME']
        password = settings.HERA['PASSWORD']
        location = settings.HERA['LOCATION']

        assert username and password and location

    except (KeyError, AttributeError, AssertionError):
        log.debug("Attempted to connect to Hera, but it's not configured.")
        return False

    try:
        hera = Hera(username, password, location)

        # This just does a request to Zeus to see if the credentials are
        # correct.  I would love to have a better way of doing this, but I don't
        # see one in the API.
        hera.getGlobalCacheInfo()

    except Exception, e:
        # suds throws generic exceptions...
        log.debug("Attempted to connect to Hera, but failed: %s", e)
        return False

    return hera


def flush_urls(urls, prefix="", return_list=False):
    hera = get_hera()

    if not hera:
        return False

    flushed = []

    for url in urls:
        pattern = "%s%s" % (prefix, url)
        r = hera.flushObjectsByPattern(pattern, return_list)
        if return_list:
            log.debug("Flushed %d URLs matching: %s" % (len(r), pattern))
            flushed += r
        else:
            log.debug("Flushed URLs matching: %s" % (pattern))


    if return_list:
        return flushed
