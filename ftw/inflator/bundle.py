from Products.CMFPlone.factory import _DEFAULT_PROFILE
from Products.CMFPlone.factory import addPloneSite
from ftw.inflator.interfaces import EXTENSION_PROFILES
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

    def install(self, app, site_id, title=None, language='en',
                extension_profiles=EXTENSION_PROFILES):

        if title is None:
            title = self.title

        extension_profiles = list(extension_profiles)
        extension_profiles.extend(self.profiles)

        return addPloneSite(
            app,
            site_id,
            title=title,
            profile_id=self.base,
            extension_ids=extension_profiles,
            setup_content=False,
            default_language=language)


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


def get_bundle_by_name(name):
    """Returns the bundle with the name `name`.
    """
    matches = filter(lambda bundle: bundle.title == name,
                     get_bundles())

    if len(matches) == 0:
        raise ValueError('No bundle found with name %s' % name)
    elif len(matches) > 1:
        raise ValueError('Too many bundles found with name %s' % name)

    return matches[0]
