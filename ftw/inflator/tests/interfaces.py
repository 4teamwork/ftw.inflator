from plone.app.textfield import RichText
from plone.directives.form import Schema
from plone.namedfile.field import NamedImage
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import Interface
from ftw.testing import IS_PLONE_5


class IFoo(Interface):
    """Mark it foo!
    """

if not IS_PLONE_5:
    from plone.formwidget.contenttree import ObjPathSourceBinder

    class IExampleDxType(Schema):
        image = NamedImage(
            title=u'Image',
        )

        relation = RelationChoice(
            title=u'Relation',
            source=ObjPathSourceBinder(),
        )

        date = schema.Date(
            title=u'Date',
            required=False,
        )

        datetime = schema.Datetime(
            title=u'Datetime',
            required=False,
        )

        richtext = RichText(
            title=u'Richtext',
            required=False,
        allowed_mime_types=('text/html',))

else:
    from plone.app.vocabularies.catalog import CatalogSource

    class IExampleDxType(Schema):
        image = NamedImage(
            title=u'Image',
        )

        relation = RelationChoice(
            title=u"Section",
            source=CatalogSource(),
        )

        date = schema.Date(
            title=u'Date',
            required=False,
        )

        datetime = schema.Datetime(
            title=u'Datetime',
            required=False,
        )

        richtext = RichText(
            title=u'Richtext',
            required=False,
            allowed_mime_types=('text/html',))
