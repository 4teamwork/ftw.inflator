from ftw.inflator.customization import InflatorCustomization
from ftw.inflator.interfaces import IInflatorCustomization
from unittest2 import TestCase
from zope.interface.verify import verifyClass


class TestCustomizationUtility(TestCase):

    def test_customization_implements_interface(self):
        self.assertTrue(IInflatorCustomization.implementedBy(InflatorCustomization))
        verifyClass(IInflatorCustomization, InflatorCustomization)

    def test_stores_arguments(self):
        obj = InflatorCustomization(product=u'foo',
                                    image='++resource++bar.jpg',
                                    order=7)

        self.assertEqual(obj.product, u'foo')
        self.assertEqual(obj.image, '++resource++bar.jpg')
        self.assertEqual(obj.order, 7)

    def test_defaults(self):
        obj = InflatorCustomization()

        self.assertEqual(obj.product, None)
        self.assertEqual(obj.image, None)
        self.assertEqual(obj.order, 10)
