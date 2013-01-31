from Products.CMFPlone.factory import _DEFAULT_PROFILE
from ftw.inflator.interfaces import IInflatorBundle
from zope.interface import implements


class InflatorBundle(object):
    """Inflator bundle utility with information about the bundle.
    """

    implements(IInflatorBundle)

    def __init__(self, title, profiles, description=u'', base=_DEFAULT_PROFILE,
                 standard=False):
        self.title = title
        self.profiles = profiles
        self.description = description
        self.base = base
        self.standard = standard
