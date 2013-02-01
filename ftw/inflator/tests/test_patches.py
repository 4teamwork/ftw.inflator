from ftw.inflator.testing import ZOPE_FUNCTIONAL_TESTING
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
from plone.testing import zca
from plone.testing.z2 import Browser
from plone.testing.z2 import zopeApp
from unittest2 import TestCase
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

            self.browser = Browser(app)
            self.browser.handleErrors = False
            self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                    SITE_OWNER_NAME, SITE_OWNER_PASSWORD))

    def tearDown(self):
        zca.popGlobalRegistry()
        self.configurationContext = None

    def load_zcml_string(self, zcml):
        xmlconfig.string(zcml, context=self.configurationContext)

    def test_add_plone_site_button_still_tehere(self):
        self.browser.open('http://localhost/manage_main')
        self.assertTrue(self.browser.getControl('Add Plone Site'))

    def test_default_inflator_install_plone_buttton(self):
        self.browser.open('http://localhost/manage_main')
        self.assertTrue(self.browser.getControl('Install Plone'))

    def test_customized_inflator_install_buttton(self):
        self.load_zcml_string('\n'.join((
                    '<configure xmlns:inflator="http://namespaces.zope.org/inflator"'
                    '           i18n_domain="my.package">',
                    '    <inflator:customize',
                    '        product="my product" />',
                    '</configure>'
                    )))

        self.browser.open('http://localhost/manage_main')
        self.assertTrue(self.browser.getControl('Install my product'))
