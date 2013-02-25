# pylint: disable=E0211, E0213
# E0211: Method has no argument
# E0213: Method should have "self" as first argument

from Products.CMFPlone.factory import _DEFAULT_PROFILE
from zope.interface import Interface
from zope.schema import Bool
from zope.schema import List
from zope.schema import TextLine


# these profiles will be installed automatically
EXTENSION_PROFILES = (
    'plonetheme.classic:default',
    'plonetheme.sunburst:default',
    )


class IInflatorBundle(Interface):
    """Marker interface for inflator bundle utilties.
    """

    def __init__(title, profiles, description=u'', base=_DEFAULT_PROFILE,
                 standard=False):
        """Stores the arguments as attributes.
        """

    def install(app, site_id, title=None, language='en',
                extension_profiles=None):
        """Installs a new plone site and returns it.
        """

    title = TextLine(
        title=u'Title',
        description=u'Bundle title.')

    profiles = List(
        title=u'Profiles',
        description=u'Generic setup profile names (without profile- prefix)',
        value_type=TextLine())

    description = TextLine(
        title=u'Description',
        description=u'Optional description for the bundle.')

    base = TextLine(
        title=u'Generic Setup base profile',
        description=u'Used as base profile when creating the site.'
            u' Defaults to %s' % _DEFAULT_PROFILE)

    standard = Bool(
        title=u'Standard profile',
        description=u'Standard profiles are listed below'
        u' non-standard profiles.')


class IInflatorCustomization(Interface):
    """Adapter interface for inflator customizations adapter.
    """

    def __init__(product=None, image=None, order=10):
        """Adapts the zope application.
        """

    product = TextLine(
        title=u'Product title',
        description=u'The title of the product to be used for the wizard.')

    image = TextLine(
        title=u'The resource name of the image',
        description=u'e.g. ++resources++the-image-1.jpg')
