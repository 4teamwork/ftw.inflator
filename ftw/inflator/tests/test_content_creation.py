from ftw.inflator.testing import INFLATOR_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from unittest2 import TestCase


class FooCreationLayer(PloneSandboxLayer):

    defaultBases = (INFLATOR_FIXTURE, )
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.inflator.tests:foo_creation')


FOO_FIXTURE = FooCreationLayer()
FOO_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FOO_FIXTURE, ), name="ftw.inflator:FOO Integration")


class TestContentCreation(TestCase):

    layer = FOO_INTEGRATION_TESTING

    def setUp(self):
        super(TestContentCreation, self).setUp()
        self.portal = self.layer['portal']

    def test_foo_folder_type(self):
        foo = self.portal.get('foo')
        self.assertNotEqual(foo, None, 'Folder /foo not created')

        self.assertEqual(
            foo.portal_type, 'Folder',
            '/foo has wrong type "%s" but should be "Folder"' % (
                foo.portal_type))

    def test_foo_folder_title(self):
        foo = self.portal.get('foo')
        self.assertNotEqual(foo, None, 'Folder /foo not created')

        self.assertEqual(
            foo.Title(), 'Foo',
            '/foo has wrong Title "%s" but should be "Foo"' % foo.Title())
