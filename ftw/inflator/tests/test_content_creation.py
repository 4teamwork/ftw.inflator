from ftw.inflator import IS_PLONE_APP_MULTILINGUAL_2
from ftw.inflator.testing import INFLATOR_FIXTURE
from ftw.inflator.tests.interfaces import IFoo
from ftw.testing import IS_PLONE_5
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.constants import GROUP_CATEGORY
from plone.portlets.constants import USER_CATEGORY
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from unittest import TestCase
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
from zope.component import getUtility


if IS_PLONE_5 or IS_PLONE_APP_MULTILINGUAL_2:
    from plone.app.dexterity.behaviors import constrains as constraintypes
    from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
else:
    from Products.ATContentTypes.lib import constraintypes


class FooCreationLayer(PloneSandboxLayer):

    defaultBases = (INFLATOR_FIXTURE, )

    def setUpPloneSite(self, portal):
        wftool = getToolByName(portal, 'portal_workflow')
        wftool.setChainForPortalTypes(['Folder'],
                                      'simple_publication_workflow')

        if IS_PLONE_5 or IS_PLONE_APP_MULTILINGUAL_2:
            folder_fti = portal.portal_types.Folder
            folder_fti.behaviors = tuple(
                list(folder_fti.behaviors) + ['plone.constraintypes']
            )

        applyProfile(portal, 'ftw.inflator:setup-language')
        applyProfile(portal, 'ftw.inflator.tests:foo_creation')


FOO_FIXTURE = FooCreationLayer()
FOO_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FOO_FIXTURE, ), name="ftw.inflator:FOO Integration")


class TestContentCreation(TestCase):

    layer = FOO_INTEGRATION_TESTING

    def setUp(self):
        super(TestContentCreation, self).setUp()
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

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

    def test_foo_folder_catalog(self):
        foo_path = '/'.join(self.portal.get('foo').getPhysicalPath())
        query = {'path': {'query': foo_path,
                          'depth': 0}}

        catalog = getToolByName(self.portal, 'portal_catalog')
        brains = catalog.unrestrictedSearchResults(query)
        self.assertEqual(len(brains), 1)

        foo_brain = brains[0]
        self.assertEqual(foo_brain.portal_type, 'Folder')
        self.assertEqual(foo_brain.Title, 'Foo')

    def test_foo_folder_workflow_state(self):
        foo = self.portal.get('foo')
        context_state = foo.unrestrictedTraverse('@@plone_context_state')
        review_state = context_state.workflow_state()
        self.assertEqual(review_state, 'published')

    def test_foo_folder_properties(self):
        foo = self.portal.get('foo')
        self.assertEqual(foo.getProperty('f\xc3\xbc\xc3\xbc'), 'b\xc3\xa4r')

    def test_foo_folder_constraintypes(self):
        foo = self.portal.get('foo')

        if IS_PLONE_5 or IS_PLONE_APP_MULTILINGUAL_2:
            constrains = ISelectableConstrainTypes(foo)
            self.assertEqual(constrains.getConstrainTypesMode(),
                             constraintypes.ENABLED,
                             'Constraint types are not enabled on folder foo')

            self.assertItemsEqual(constrains.getImmediatelyAddableTypes(),
                                  ['Folder'],
                                  'Immediately addable types are not configured well')

            self.assertItemsEqual(constrains.getLocallyAllowedTypes(),
                                  ['Folder', 'Document'],
                                  'Locally addable types are not configured well')

        else:
            self.assertEqual(foo.getConstrainTypesMode(),
                             constraintypes.ENABLED,
                             'Constraint types are not enabled on folder foo')

            self.assertEqual(foo.getImmediatelyAddableTypes(),
                             ('Folder',),
                             'Immediately addable types are not configured well')

            self.assertEqual(foo.getLocallyAllowedTypes(),
                             ('Folder', 'Document'),
                             'Locally addable types are not configured well')

    def test_foo_folder_interfaces(self):
        foo = self.portal.get('foo')

        self.assertTrue(IFoo.providedBy(foo),
                        'IFoo interface not provided by Folder foo')

    def test_file_inserted(self):
        foo = self.portal.get('foo')
        files = foo.get('files')
        example_file = files.get('example-file')

        self.assertTrue(example_file)
        self.assertEqual(example_file.Title(), 'example file')

        if IS_PLONE_5 or IS_PLONE_APP_MULTILINGUAL_2:
            data = example_file.file
            self.assertEqual(data.filename, 'examplefile.txt')
            self.assertEqual(data.contentType, 'text/plain')
        else:
            data = example_file.getField('file').get(example_file)
            self.assertEqual(data.getFilename(), 'examplefile.txt')
            self.assertEqual(data.getContentType(), 'text/plain')

        self.assertEqual(data.data, 'a simple text file')

    def test_intranet_placeful_workflow(self):
        intranet = self.portal.get('foo').get('intranet')

        wftool = getToolByName(self.portal, 'portal_workflow')
        workflows = wftool.getWorkflowsFor(intranet)
        self.assertEqual(len(workflows), 1)
        wfid = workflows[0].id
        self.assertEqual(wfid, 'intranet_folder_workflow')

    def test_annotations(self):
        foo = self.portal.get('foo')
        intranet = foo.get('intranet')

        annotations = IAnnotations(intranet)
        self.assertEqual(annotations.get('foo'), {
                'bar': [1, 2, 'three'],
                'baz': True})

        self.assertFalse(isinstance({}, PersistentMapping))
        self.assertTrue(isinstance(annotations.get('foo'),
                                   PersistentMapping))

        self.assertFalse(isinstance({}, PersistentList))
        self.assertTrue(isinstance(annotations.get('foo').get('bar'),
                                   PersistentList))

    def test_intranet_translated_title(self):
        intranet = self.portal.get('foo').get('intranet')
        self.assertEqual(intranet.Title(), 'Intranet')

    def test_resolve_uuid(self):
        foo = self.portal.get('foo')
        foo_uuid = IUUID(foo)

        files = foo.get('files')
        annotations = IAnnotations(files)

        self.assertEquals(annotations.get('relative-parent-uuid'), foo_uuid)
        self.assertEquals(annotations.get('absolute-parent-uuid'), foo_uuid)

    def test_image_object(self):
        chuck = self.portal.get('foo').get('files').get('chuck-norris')
        self.assertTrue(chuck,
                        'Where is chuck norris? Image object not'
                        ' found under /foo/files/chuck-norris')

        self.assertEquals('Chuck Norris', chuck.Title())

        if IS_PLONE_5 or IS_PLONE_APP_MULTILINGUAL_2:
            self.assertTrue(chuck.image.getSize(),
                            'The chuck norris image seems to be missing')
            self.assertEquals(chuck.image._width, 319)
            self.assertEquals(chuck.image._height, 397)

        else:
            self.assertTrue(chuck.getSize(), 'The chuck norris image seems to be missing')
            self.assertEquals(chuck.getWidth(), 319)
            self.assertEquals(chuck.getHeight(), 397)

    def test_filename_can_be_changed(self):
        obj = self.portal.get('foo').get('files').get('filename-changed')

        if IS_PLONE_5 or IS_PLONE_APP_MULTILINGUAL_2:
            self.assertEquals('filename-has-changed.jpg',
                              obj.image.filename)
        else:
            self.assertEquals('filename-has-changed.jpg',
                              obj.getImage().getFilename())

    def test_news_item_object(self):
        item = self.portal.get('foo').get('in-other-news')
        self.assertTrue(item, 'Missing News Item at foo/in-other-news')

        self.assertEquals('In other news', item.Title(), 'Wrong News Item title')

        if IS_PLONE_5 or IS_PLONE_APP_MULTILINGUAL_2:
            self.assertTrue(item.text.raw, 'News item has no text')
        else:
            self.assertTrue(item.getText(), 'News item has no text')

    def test_local_roles_are_created(self):
        obj = self.portal.get('foo')
        roles = dict(obj.get_local_roles())
        self.assertEqual(("Owner", "Contributor", "Editor",),
                         roles.get("admin"))
        self.assertEqual(("Editor",), roles.get("hans"))

    def test_block_local_roles(self):
        obj = self.portal.get('foo')
        self.assertTrue(obj.__ac_local_roles_block__)

        intranet = obj.get('intranet')
        self.assertFalse(hasattr(intranet, '__ac_local_roles_block__'))

    def test_adding_portlets(self):
        obj = self.portal.get('foo')
        manager = getUtility(IPortletManager, 'plone.leftcolumn')
        mapping = getMultiAdapter((obj, manager), IPortletAssignmentMapping)

        self.assertEquals(1, len(mapping))

        portlet = mapping.get('new_navigation')
        self.assertEquals('New Navigation', portlet.name)
        self.assertEquals(0, portlet.bottomLevel)
        self.assertEquals(False, portlet.includeTop)
        self.assertEquals(1, portlet.topLevel)

    def test_set_blacklists_correctly(self):
        obj = self.portal.get('foo')
        manager = getUtility(IPortletManager, 'plone.leftcolumn')
        assignable = getMultiAdapter((obj, manager),
                                     ILocalPortletAssignmentManager)

        self.assertTrue(assignable.getBlacklistStatus(CONTEXT_CATEGORY))
        self.assertFalse(assignable.getBlacklistStatus(USER_CATEGORY))
        self.assertIsNone(assignable.getBlacklistStatus(GROUP_CATEGORY))
