import os
from urlparse import urlparse

from suds.client import Client
from suds.transport.http import HttpAuthenticated
from suds.xsd.doctor import ImportDoctor, Import

class Hera:

    def __init__(self, username, password, location, wsdl="System.Cache.wsdl"):

        # Sorry windows
        cur = os.path.dirname(__file__)
        url = "file://%s" % os.path.abspath(os.path.join(cur, 'wsdl', wsdl))

        # Apparently Zeus's wsdl is broken and we have to jimmy this thing in
        # manually.  See https://fedorahosted.org/suds/ticket/220 for details.
        # Also, you'll be happy to know that the zillion .wsdl files that Zeus
        # includes apparently have different targetNamespace's.  This one
        # happens to be 1.1, but if you load something else you'll probably
        # need to adjust it.
        imp = Import('http://schemas.xmlsoap.org/soap/encoding/')
        imp.filter.add('http://soap.zeus.com/zxtm/1.1/')
        doctor = ImportDoctor(imp)

        transporter = HttpAuthenticated(username=username, password=password)

        self.client = Client(url, doctor=doctor, location=location,
                             transport=transporter)

    def flushAll(self):
        """Flushes everything in the system: all objects across all virtual
        servers."""
        return self.client.service.clearWebCache()


    def getGlobalCacheInfo(self):
        """Returns a small object of statistics."""
        return self.client.service.getGlobalCacheInfo()


    def flushObjectsByPattern(self, url, return_list=False):
        """Flush objects out of the cache.  This accepts simple wildcards (*)
        in the host and/or path.  If return_list is True we'll return a list of
        URLs that matched the pattern.  There is a performance hit when
        returning the list since we have to request it, build it, and return
        it.  """
        if return_list:
            objects = self.getObjectsByPattern(url)

        o = urlparse(url)
        r = self.client.service.clearMatchingCacheContent(o.scheme,
                                                          o.netloc,
                                                          o.path)
        if return_list and objects:
            return ["%s://%s%s" % (o.protocol, o.host, o.path)
                    for o in objects]
        else:
            return []


    def getObjectByPattern(self, url):
        """A simple convenience function.  If you have a full URL and you want
        a single object back, this is the one."""
        return self.getObjectsByPattern(url, 1)

    def getObjectsByPattern(self, url, limit=None):
        o = urlparse(url)
        r = self.client.service.getCacheContent(o.scheme, o.netloc,
                                                o.path, limit)

        if r.number_matching_items:
            return r.matching_items
