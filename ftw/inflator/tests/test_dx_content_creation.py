from Products.CMFCore.utils import getToolByName
from ftw.inflator.testing import INFLATOR_FIXTURE
from ftw.inflator.tests.interfaces import IFoo
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from unittest2 import TestCase
from zope.annotation.interfaces import IAnnotations
from zope.configuration import xmlconfig


class DXCreationLayer(PloneSandboxLayer):

    defaultBases = (INFLATOR_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import plone.app.dexterity
        xmlconfig.file('configure.zcml', plone.app.dexterity,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        wftool = getToolByName(portal, 'portal_workflow')
        wftool.setChainForPortalTypes(['ExampleDxType'],
                                      'simple_publication_workflow')

        applyProfile(portal, 'ftw.inflator:setup-language')
        applyProfile(portal, 'ftw.inflator.tests:dx_creation')


DX_FIXTURE = DXCreationLayer()
DX_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DX_FIXTURE, ), name="ftw.inflator:DX Integration")


class TestDXContentCreation(TestCase):

    layer = DX_INTEGRATION_TESTING

    def setUp(self):
        super(TestDXContentCreation, self).setUp()
        self.portal = self.layer['portal']

    def test_object_is_there(self):
        self.assertTrue(self.portal.get('my-dx'))

    def test_title(self):
        obj = self.portal.get('my-dx')
        self.assertEquals(obj.Title(), 'My Dexterity Object')

    def test_catalog(self):
        obj_path = '/'.join(self.portal.get('my-dx').getPhysicalPath())
        query = {'path': {'query': obj_path,
                          'depth': 0}}

        catalog = getToolByName(self.portal, 'portal_catalog')
        brains = catalog.unrestrictedSearchResults(query)
        self.assertEqual(len(brains), 1)

        obj_brain = brains[0]
        self.assertEqual(obj_brain.portal_type, 'ExampleDxType')
        self.assertEqual(obj_brain.Title, 'My Dexterity Object')

    def test_properties(self):
        obj = self.portal.get('my-dx')
        self.assertEqual(obj.getProperty('f\xc3\xbc\xc3\xbc'), 'b\xc3\xa4r')

    def test_interfaces(self):
        obj = self.portal.get('my-dx')

        self.assertTrue(IFoo.providedBy(obj),
                        'IFoo interface not provided by Object my-dx')

    def test_annotations(self):
        obj = self.portal.get('my-dx')
        annotations = IAnnotations(obj)
        self.assertEqual(annotations.get('foo'), {
                'bar': [1, 2, 'three'],
                'baz': True})

        self.assertFalse(isinstance({}, PersistentMapping))
        self.assertTrue(isinstance(annotations.get('foo'),
                                   PersistentMapping))

        self.assertFalse(isinstance({}, PersistentList))
        self.assertTrue(isinstance(annotations.get('foo').get('bar'),
                                   PersistentList))

    def test_local_roles_are_created(self):
        obj = self.portal.get('my-dx')
        roles = dict(obj.get_local_roles())
        self.assertEqual(("Owner", "Contributor", "Editor",),
                         roles.get("admin"))
        self.assertEqual(("Editor",), roles.get("hans"))

    def test_paths_are_resolved(self):
        obj = self.portal.get('my-dx')
        target = self.portal.get('target')
        self.assertEqual(obj.relation, target)
