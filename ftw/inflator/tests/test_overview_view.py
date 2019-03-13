from ftw.inflator.testing import ZOPE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.app.testing import SITE_OWNER_NAME
from plone.testing.z2 import zopeApp
from unittest2 import TestCase


class TestInflateOverView(TestCase):

    layer = ZOPE_FUNCTIONAL_TESTING

    def setUp(self):
        with zopeApp() as app:
            self.app = app

    def tearDown(self):
        del self.app

    @browsing
    def test_overview_view(self, browser):
        browser.login(SITE_OWNER_NAME).open('http://localhost/index_html')
        browser.click_on('Create a new Plone site')
        self.assertTrue(browser.url.startswith('http://localhost/@@inflate'))
