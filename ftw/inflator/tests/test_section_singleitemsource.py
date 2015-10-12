from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from ftw.inflator.creation.sections import singleitemsource
from unittest2 import TestCase
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject


class TestSingleItemSource(TestCase):

    def test_implements_interface(self):
        klass = singleitemsource.SingleItemSource

        self.assertTrue(ISection.implementedBy(klass),
                        'Class %s does not implement ISection.' % str(klass))
        verifyClass(ISection, klass)

        self.assertTrue(ISectionBlueprint.providedBy(klass),
                        'Class %s does not provide ISectionBlueprint.' % (
                str(klass)))
        verifyObject(ISectionBlueprint, klass)

    def test_yields_item_from_options(self):
        source = singleitemsource.SingleItemSource(
            None, '', {'item': {'foo': 'bar'}}, ())

        self.assertEqual([{'foo': 'bar'}], list(source))
