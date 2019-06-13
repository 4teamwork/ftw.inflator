from ftw.inflator.tests.interfaces import IExampleDxType
from plone.dexterity.content import Item
from plone.dexterity.content import Container
from zope.interface import implements


class ExampleDxContainerType(Container):
    implements(IExampleDxType)


class ExampleDxType(Item):
    implements(IExampleDxType)
