from Products.CMFCore.utils import getToolByName
from ftw.inflator.testing import ZOPE_FUNCTIONAL_TESTING
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser
from plone.testing.z2 import zopeApp
from unittest2 import TestCase


class TestInflateView(TestCase):

    layer = ZOPE_FUNCTIONAL_TESTING

    def setUp(self):
        with zopeApp() as app:
            self.app = app

            self.browser = Browser(app)
            self.browser.handleErrors = False
            self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                    SITE_OWNER_NAME, SITE_OWNER_PASSWORD))

    def test_add_plone_site_button_still_tehere(self):
        self.browser.open('http://localhost/@@inflate')
        self.assertIn('++resource++inflator-plone-logo-0.png',
                      self.browser.contents)

    def test_default_form_values(self):
        self.browser.open('http://localhost/@@inflate')

        # default values
        self.assertEquals(self.browser.getControl(name='site_id').value,
                          'platform')

        self.assertEquals(self.browser.getControl(name='title').value,
                          'Plone')

        self.assertEquals(
            self.browser.getControl(name='default_language').value,
            ['en'])

        self.assertEquals(
            self.browser.getControl(name='bundle').value,
            ['ftw.inflator example bundle one'])

    def test_install_test_profile(self):
        self.browser.open('http://localhost/@@inflate')

        self.browser.getControl(name='default_language').value = ['de']
        self.browser.getControl('Install').click()
        self.assertEqual(self.browser.url, 'http://localhost/platform')

        site = self.app.get('platform')
        self.assertTrue(site)

        language_tool = getToolByName(site, 'portal_languages')
        self.assertEqual(language_tool.getDefaultLanguage(), 'de')
