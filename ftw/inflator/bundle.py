from Products.CMFPlone.factory import _DEFAULT_PROFILE
from ftw.inflator.interfaces import IInflatorBundle
from zope.component import getUtilitiesFor
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


def get_bundles():
    """Returns a list of all registered bundles.
    """

    def sort_key(item):
        name, bundle = item
        if bundle.standard:
            return 1, name
        else:
            return 0, name

    bundles = sorted(getUtilitiesFor(IInflatorBundle),
                     key=sort_key)

    return [bundle for (_name, bundle) in bundles]
