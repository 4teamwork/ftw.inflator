from ftw.inflator.testing import ZOPE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.testing.z2 import zopeApp
from unittest2 import TestCase
from zope.component.hooks import setSite


class TestInflateView(TestCase):

    layer = ZOPE_FUNCTIONAL_TESTING

    def setUp(self):
        with zopeApp() as app:
            self.app = app

    def tearDown(self):
        del self.app

    @browsing
    def test_add_plone_site_button_still_tehere(self, browser):
        browser.login(SITE_OWNER_NAME).open('http://localhost/@@inflate')
        self.assertEquals('++resource++inflator-plone-logo-0.png',
                          browser.css('.header img').first.attrib['src'])

    @browsing
    def test_default_form_values(self, browser):
        browser.login(SITE_OWNER_NAME).open('http://localhost/@@inflate')

        # default values
        self.assertEquals('platform', browser.find('Path identifier').value)
        self.assertEquals('Plone', browser.find('title').value)
        self.assertEquals('en', browser.find('default_language').value)
        self.assertEquals('ftw.inflator example bundle one', browser.find('bundle').value)

    @browsing
    def test_install_test_profile(self, browser):
        browser.login(SITE_OWNER_NAME).open('http://localhost/@@inflate')

        browser.fill({'default_language': 'de'})
        browser.click_on('Install')
        self.assertEqual('http://localhost/platform', browser.url)

        site = self.app.get('platform')
        self.assertTrue(site)

        setSite(site)
        language_tool = api.portal.get_tool('portal_languages')
        self.assertEqual(language_tool.getDefaultLanguage(), 'de')
