from Products.CMFPlone.factory import _DEFAULT_PROFILE
from Products.Five.browser.metaconfigure import resource
from ftw.inflator.bundle import InflatorBundle
from ftw.inflator.customization import InflatorCustomization
from ftw.inflator.interfaces import IInflatorBundle
from ftw.inflator.interfaces import IInflatorCustomization
from zope.component.zcml import handler
from zope.configuration.fields import Bool
from zope.configuration.fields import MessageID
from zope.configuration.fields import Path
from zope.configuration.fields import Tokens
from zope.interface import Interface
from zope.schema import Int
from zope.schema import TextLine
import os.path


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
        description=u'Used as base profile when creating the site.'
        u' Defaults to %s' % _DEFAULT_PROFILE,
        default=_DEFAULT_PROFILE.decode('utf-8'),
        required=False)

    standard = Bool(
        title=u'Standard profile',
        description=u'Standard profiles are listed below'
        u' non-standard profiles.',
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


class IRegisterCustomizationDirective(Interface):

    product = MessageID(
        title=u'Product title',
        default=None,
        required=False)

    image = Path(
        title=u'Path to the logo image',
        default=None,
        required=False)

    order = Int(
        title=u'Customization odering number',
        default=10,
        required=False)


def registerCustomization(_context, **kwargs):
    """Register a customization.
    """
    name = str(kwargs.get('order', 10))

    if 'image' in kwargs:
        image_path = kwargs['image']
        basename, ext = os.path.splitext(os.path.basename(image_path))
        resourcename = 'inflator-%s-%s%s' % (basename, name, ext)
        resource(_context, resourcename, file=image_path)
        kwargs['image'] = '++resource++%s' % resourcename.encode('utf-8')

    component = InflatorCustomization(**kwargs)
    provides = IInflatorCustomization

    _context.action(
        discriminator=('bundle', name),
        callable=handler,
        args=('registerUtility', component, provides, name))
