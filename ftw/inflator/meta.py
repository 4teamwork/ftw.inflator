from Products.CMFPlone.factory import _DEFAULT_PROFILE
from ftw.inflator.bundle import InflatorBundle
from ftw.inflator.interfaces import IInflatorBundle
from zope.component.zcml import handler
from zope.configuration.fields import Bool
from zope.configuration.fields import MessageID
from zope.configuration.fields import Tokens
from zope.interface import Interface
from zope.schema import TextLine


class IRegisterBundleDirective(Interface):

    title = MessageID(
        title=u'Title',
        description=u'Bundle title.',
        default=None,
        required=True)

    profiles = Tokens(
        title=u'Profiles',
        description=u'Generic setup profile names (without profile- prefix)',
        default=None,
        required=True,
        value_type=TextLine())

    description = MessageID(
        title=u'Description',
        description=u'Optional description for the bundle.',
        default=u'',
        required=False)

    base = TextLine(
        title=u'Generic Setup base profile',
        description=u'Used as base profile when creating the site. ' + \
            u'Defaults to %s' % _DEFAULT_PROFILE,
        default=_DEFAULT_PROFILE.decode('utf-8'),
        required=False)

    standard = Bool(
        title=u'Standard profile',
        description=u'Standard profiles are listed below non-standard profiles.',
        default=False,
        required=False)


def registerBundle(_context, **kwargs):
    """Register a bundle.
    """

    component = InflatorBundle(**kwargs)
    provides = IInflatorBundle
    name = kwargs['title']

    _context.action(
        discriminator=('bundle', name),
        callable=handler,
        args=('registerUtility', component, provides, name),
        kw={'factory': None})
