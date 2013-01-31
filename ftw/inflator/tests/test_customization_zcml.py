from ftw.inflator.customization import get_merged_customizations
from ftw.inflator.testing import ZOPE_LAYER
from plone.testing import z2
from plone.testing import zca
from unittest2 import TestCase
from zope.configuration import xmlconfig


class TestCustomizationZCML(TestCase):

    layer = ZOPE_LAYER

    def setUp(self):
        zca.pushGlobalRegistry()
        self.configurationContext = zca.stackConfigurationContext()

        import ftw.inflator
        xmlconfig.file('meta.zcml', ftw.inflator, context=self.configurationContext)

    def tearDown(self):
        zca.popGlobalRegistry()
        self.configurationContext = None

    def load_zcml_string(self, zcml):
        xmlconfig.string(zcml, context=self.configurationContext)

    def test_customize_product_name(self):
        self.load_zcml_string('\n'.join((
                    '<configure xmlns:inflator="http://namespaces.zope.org/inflator"'
                    '           i18n_domain="my.package">',
                    '    <inflator:customize',
                    '        product="my product" />',
                    '</configure>'
                    )))

        self.assertEquals(get_merged_customizations().product, u'my product')

    def test_customize_image(self):
        self.load_zcml_string('\n'.join((
                    '<configure xmlns:inflator="http://namespaces.zope.org/inflator"'
                    '           i18n_domain="my.package"'
                    '           package="ftw.inflator.tests">',
                    '    <inflator:customize',
                    '        image="../resources/plone-logo.png" />',
                    '</configure>'
                    )))

        image = get_merged_customizations().image
        self.assertEquals(image, '++resource++inflator-plone-logo-10.png')

        with z2.zopeApp() as app:
            self.assertTrue(app.unrestrictedTraverse(image))

    def test_merging_cusetomizations(self):
        self.load_zcml_string('\n'.join((
                    '<configure xmlns:inflator="http://namespaces.zope.org/inflator"'
                    '           i18n_domain="my.package"'
                    '           package="ftw.inflator.tests">',

                    '    <inflator:customize',
                    '        product="foo"'
                    '        image="../resources/plone-logo.png"'
                    '        order="4"/>',

                    '    <inflator:customize',
                    '        product="bar"'
                    '        order="5"/>',

                    '</configure>'
                    )))

        customizations = get_merged_customizations()
        self.assertEquals(customizations.image, '++resource++inflator-plone-logo-4.png')
        self.assertEquals(customizations.product, 'bar')

    def test_defaults(self):
        customizations = get_merged_customizations()
        self.assertEquals(customizations.image, '++resource++inflator-plone-logo-0.png')
        self.assertEquals(customizations.product, 'Plone')
