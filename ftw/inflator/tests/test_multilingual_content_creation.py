from Products.CMFCore.utils import getToolByName
from ftw.inflator.testing import INFLATOR_FUNCTIONAL_TESTING
from plone.app.testing import applyProfile
from plone.multilingual.interfaces import ITranslationManager
from unittest2 import TestCase


class TestMultilingualContentCreation(TestCase):

    layer = INFLATOR_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestMultilingualContentCreation, self).setUp()
        self.portal = self.layer['portal']

        wftool = getToolByName(self.portal, 'portal_workflow')
        # Folder is the default language folder type, for which
        # plone.app.multilingual's setup expects a "publish" transition.
        wftool.setChainForPortalTypes(['Folder'],
                                      'simple_publication_workflow')

        applyProfile(self.portal, 'ftw.inflator:setup-language')
        applyProfile(self.portal, 'plone.app.multilingual:default')
        applyProfile(self.portal, 'ftw.inflator.tests:multilingual_creation')

    def test_language_folder_properties_are_set(self):
        obj = self.portal.get('de')
        self.assertEqual(obj.getProperty('layout'), 'there')

    def test_content_creation_from_flat_translated_json(self):
        parent = self.portal.get('en').get('accessibility')
        folder = parent.get('folderwithpath')

        self.assertIsNotNone(folder,
                            'Missing en/accessibility/folderwithpath')
        self.assertEquals('Folder', folder.Title())

        parent = self.portal.get('de').get('barrierefreiheit')
        folder = parent.get('ordnermitpfad')

        self.assertIsNotNone(folder,
                             'Missing de/barrierefreiheit/ordnermitpfad')
        self.assertEquals('Ordner', folder.Title())

    def test_sets_up_language_folders(self):
        self.assertIsNotNone(self.portal.get('en'),
                        'Expected English language folder at /en')

        self.assertIsNotNone(self.portal.get('de'),
                        'Expected German language folder at /de')

    def test_content_is_translated_into_respective_language(self):
        english_content = self.portal.get('en').get('accessibility')
        self.assertIsNotNone(english_content, 'Missing page /en/accessibility')
        self.assertEquals('Accessibility', english_content.Title())

        german_content = self.portal.get('de').get('barrierefreiheit')
        self.assertIsNotNone(german_content,
                            'Missing page /de/barrierefreiheit')
        self.assertEquals('Barrierefreiheit', german_content.Title())

    def test_multilingual_content_is_linked(self):
        english_content = self.portal.get('en').get('accessibility')
        self.assertIsNotNone(english_content, 'Missing page /en/accessibility')

        german_content = self.portal.get('de').get('barrierefreiheit')
        self.assertIsNotNone(german_content,
                             'Missing page /de/barrierefreiheit')

        manager = ITranslationManager(english_content)
        self.assertEquals(german_content,
                          manager.get_translation('de'),
                          'English and German content should be linked.')

    def test_content_creation_import_step_depends_on_languagetool(self):
        # The content creation import step needs to depend on the
        # "languagetool" import step when plone.app.multilingual is installed.
        # The "languagetool" import step is not Plone core.

        setup_tool = getToolByName(self.portal, 'portal_setup')
        import_step_name = 'ftw.inflator.content_creation'
        metadata = setup_tool.getImportStepMetadata(import_step_name)
        self.assertIn('languagetool', metadata.get('dependencies', ()))
