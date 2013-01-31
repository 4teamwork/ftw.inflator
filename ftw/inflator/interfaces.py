from Products.CMFPlone.factory import _DEFAULT_PROFILE
from zope.interface import Interface
from zope.schema import Bool
from zope.schema import List
from zope.schema import TextLine


class IInflatorBundle(Interface):
    """Marker interface for inflator bundle utilties.
    """

    def __init__(title, profiles, description=u'', base=_DEFAULT_PROFILE,
                 standard=False):
        """Stores the arguments as attributes.
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
        description=u'Used as base profile when creating the site. ' + \
            u'Defaults to %s' % _DEFAULT_PROFILE)

    standard = Bool(
        title=u'Standard profile',
        description=u'Standard profiles are listed below non-standard profiles.')
