# Just a couple of helpful functions if you're using django.
import logging
import random

from django.conf import settings

from hera import Hera

log = logging.getLogger('z.hera')

def get_hera(creds={}):
    """Return a Hera object or False on failure.  If you have multiple Zeus
    boxes configured this will pick a random one unless you pass in a dictionary
    with credentials."""
    try:
        if not creds:
            creds = random.choice(settings.HERA)

        username = creds['USERNAME']
        password = creds['PASSWORD']
        location = creds['LOCATION']

        assert username and password and location

    except (IndexError, KeyError, AttributeError, AssertionError):
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

    flushed = []
    pattern = ''

    for i in settings.HERA:
        hera = get_hera(i)

        if not hera:
            # Failure already logged in get_hera()
            continue

        for url in urls:
            pattern = "%s%s" % (prefix, url)
            l = hera.flushObjectsByPattern(pattern, return_list)
            if l:
                flushed += l

    flushed = list(set(flushed))  # deduplicate

    if return_list:
        log.debug("Flushed %d URLs matching: %s" % (len(flushed), pattern))
    elif pattern:
        log.debug("Flushed URLs matching: %s" % (pattern))

    if return_list:
        return flushed
