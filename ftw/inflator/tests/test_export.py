from ftw.builder import Builder
from ftw.builder import create
from ftw.inflator.testing import INFLATOR_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import plone
from ftw.zipexport.zipfilestream import ZipFile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from unittest2 import TestCase
import json
import transaction


class TestExport(TestCase):
    layer = INFLATOR_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        transaction.commit()

    @browsing
    def test_controlpanel_is_available(self, browser):
        browser.login().open(view='overview-controlpanel')
        browser.find('Inflator export').click()
        self.assertEquals('inflator-export', plone.view())

    @browsing
    def test_export_of_objects(self, browser):
        create(Builder('page').titled('The Page'))
        folder = create(Builder('folder').titled('A Folder'))
        create(Builder('page').titled('Another Page').within(folder))

        browser.login().open(view='inflator-export')
        browser.find('Export').click()
        self.assertEquals('application/zip', browser.headers['content-type'])

        zipfile = ZipFile(StringIO(browser.contents), 'r')
        self.assertEquals(
            ['content_creation/the-page.json',
             'content_creation/a-folder.json'],
            zipfile.namelist())

    @browsing
    def test_exporting_files(self, browser):
        create(Builder('file').with_dummy_content().titled('The File'))
        browser.login().open(view='inflator-export')
        browser.find('Export').click()

        zipfile = ZipFile(StringIO(browser.contents), 'r')
        self.assertEquals(
            ['content_creation/files/the-file-file/test.doc',
             'content_creation/the-file.json'],
            zipfile.namelist())

        data = json.load(zipfile.open('content_creation/the-file.json'))
        item, = data
        self.assertDictContainsSubset(
            {u'file:file': u'files/the-file-file/test.doc'}, item)

    @browsing
    def test_roundtrip(self, browser):
        folder = create(Builder('folder').titled('A Folder'))

        create(Builder('page').titled('First Page')
               .within(folder)
               .having(text='<p>Hello World</p>'))

        create(Builder('file').titled('The File')
               .attach_file_containing('print "Hello World"', 'helloworld.py')
               .within(folder))

        second_page = create(Builder('page').titled('Second Page')
                             .having(text='<p>The Second Page</p>'))

        browser.login().open(view='inflator-export')
        browser.find('Export').click()
        zipfile = ZipFile(StringIO(browser.contents), 'r')

        self.portal.manage_delObjects([folder.getId(), second_page.getId()])

        gsprofile = Builder('genericsetup profile')
        for name in zipfile.namelist():
            gsprofile.with_file(name, zipfile.open(name).read(), makedirs=True)

        package = create(Builder('python package')
                         .at_path(self.layer['temp_directory'])
                         .named('my.package')
                         .with_profile(gsprofile))

        portal_setup = getToolByName(self.portal, 'portal_setup')
        with package.zcml_loaded(self.layer['configurationContext']):
            portal_setup.runAllImportStepsFromProfile(
                'profile-my.package:default')

        folder = self.portal.get('a-folder')
        self.assertEquals('A Folder', folder.Title())

        first_page = folder.get('first-page')
        self.assertEquals('First Page', first_page.Title())
        self.assertEquals('<p>Hello World</p>', first_page.getText())

        the_file = folder.get('the-file')
        self.assertEquals('The File', the_file.Title())
        self.assertEquals('helloworld.py', the_file.getFile().filename)
        self.assertEquals('print "Hello World"', the_file.getFile().data)

        second_page = self.portal.get('second-page')
        self.assertEquals('Second Page', second_page.Title())
        self.assertEquals('<p>The Second Page</p>', second_page.getText())
