from plone.directives.form import Schema
from plone.namedfile.field import NamedImage
from zope.interface import Interface


class IFoo(Interface):
    """Mark it foo!
    """


class IExampleDxType(Schema):
    image = NamedImage(
        title=u'Image',
        )
