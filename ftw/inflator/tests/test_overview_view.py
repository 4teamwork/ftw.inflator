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

    def test_overview_view(self):
        self.browser.open('http://localhost/index_html')
        self.browser.getControl('Create a new Plone site').click()
        self.assertEquals(self.browser.url,
                          'http://localhost/@@inflate?')
