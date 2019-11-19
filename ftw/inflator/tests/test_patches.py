from ftw.inflator.testing import ZOPE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.app.testing import SITE_OWNER_NAME
from plone.testing import zca
from plone.testing.z2 import zopeApp
from unittest import TestCase
from zope.configuration import xmlconfig


class TestZMIButton(TestCase):

    layer = ZOPE_FUNCTIONAL_TESTING

    def setUp(self):
        zca.pushGlobalRegistry()
        self.configurationContext = zca.stackConfigurationContext()

        import ftw.inflator
        xmlconfig.file('meta.zcml', ftw.inflator, context=self.configurationContext)

        with zopeApp() as app:
            self.app = app

    def tearDown(self):
        zca.popGlobalRegistry()
        self.configurationContext = None
        del self.app

    def load_zcml_string(self, zcml):
        xmlconfig.string(zcml, context=self.configurationContext)

    @browsing
    def test_add_plone_site_button_still_tehere(self, browser):
        browser.login(SITE_OWNER_NAME).open('http://localhost/manage_main')
        self.assertTrue(browser.find_button_by_label('Add Plone Site'))

    @browsing
    def test_default_inflator_install_plone_buttton(self, browser):
        browser.login(SITE_OWNER_NAME).open('http://localhost/manage_main')
        self.assertTrue(browser.find_button_by_label('Install Plone'))

    @browsing
    def test_customized_inflator_install_buttton(self, browser):
        self.load_zcml_string('\n'.join((
                    '<configure xmlns:inflator="http://namespaces.zope.org/inflator"'
                    '           i18n_domain="my.package">',
                    '    <inflator:customize',
                    '        product="my product" />',
                    '</configure>'
                    )))

        browser.login(SITE_OWNER_NAME).open('http://localhost/manage_main')
        self.assertTrue(browser.find_button_by_label('Install my product'))
