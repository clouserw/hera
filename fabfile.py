# Used just to set the PYTHONPATH so the tests can load your settings file.
import functools
import os

from fabric.api import local

ROOT = os.path.abspath(os.path.dirname(__file__))

os.environ['PYTHONPATH'] = ROOT

local = functools.partial(local, capture=False)

def test():
    local('nosetests')
