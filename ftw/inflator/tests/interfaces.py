from plone.directives.form import Schema
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.namedfile.field import NamedImage
from z3c.relationfield.schema import RelationChoice
from zope.interface import Interface


class IFoo(Interface):
    """Mark it foo!
    """


class IExampleDxType(Schema):
    image = NamedImage(
        title=u'Image',
        )

    relation = RelationChoice(
        title=u'Relation',
        source=ObjPathSourceBinder(),
        )
