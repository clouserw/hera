Hera
====

In mythology Hera was Zeus's wife (and sister!).  In this directory, Hera is an
interface to interact with a `Zeus Traffic Manager`_ (formerly ZXTM) via it's
SOAP interface.  This library was written for Traffic Manager version 6.

You can do pretty much anything you want to from the API, however, this
particular library currently only interacts with the ``System.Cache.wsdl`` since
that's the only part I'm interested in.

Zeus manuals and the complete set of WSDL files are available on each Traffic
Manager through a maze of clicking:

    1) Log in
    2) Click "Diagnose"
    3) Click "Technical Support"
    4) The manuals are all on this page as well as a link to "Control API WSDL Files"


Basic Use
---------
A simple example::

    >>> from hera import Hera

    >>> h = Hera(username, password, location)

    # Empties the entire cache
    >>> h.flushAll()


Tests
-----

Copy ``test_settings.py-dist`` to ``test_settings.py`` and fill in all the
values.  Then run ``fab test``.


.. _Zeus Traffic Manager: http://www.zeus.com/
