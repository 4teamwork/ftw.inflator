from Products.CMFPlone.factory import _DEFAULT_PROFILE
from ftw.inflator.bundle import InflatorBundle
from ftw.inflator.interfaces import IInflatorBundle
from unittest2 import TestCase
from zope.interface.verify import verifyClass


class TestBundleUtility(TestCase):

    def test_bundle_implements_interface(self):
        self.assertTrue(IInflatorBundle.implementedBy(InflatorBundle))
        verifyClass(IInflatorBundle, InflatorBundle)

    def test_stores_arguments(self):
        obj = InflatorBundle(title=u'foo',
                             profiles=[u'bar'],
                             description=u'baz',
                             base=u'foo:default',
                             standard=True)

        self.assertEqual(obj.title, u'foo')
        self.assertEqual(obj.profiles, [u'bar'])
        self.assertEqual(obj.description, u'baz')
        self.assertEqual(obj.base, u'foo:default')
        self.assertEqual(obj.standard, True)

    def test_defaults(self):
        obj = InflatorBundle(title=u'foo', profiles=[u'bar'])

        self.assertEqual(obj.title, u'foo')
        self.assertEqual(obj.profiles, [u'bar'])
        self.assertEqual(obj.description, u'')
        self.assertEqual(obj.base, _DEFAULT_PROFILE)
        self.assertEqual(obj.standard, False)

    def test_requires(self):
        with self.assertRaises(TypeError) as cm:
            InflatorBundle()

        self.assertEquals(str(cm.exception),
                          '__init__() takes at least 3 arguments (1 given)')
