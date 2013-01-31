from Products.CMFPlone.factory import _DEFAULT_PROFILE
from ftw.inflator.interfaces import IInflatorBundle
from ftw.inflator.testing import META_ZCML
from ftw.testing import MockTestCase
from zope.component import getUtilitiesFor
from zope.configuration.config import ConfigurationConflictError


class TestBundlesZCML(MockTestCase):

    layer = META_ZCML

    def get_utilites(self):
        return list(getUtilitiesFor(IInflatorBundle))

    def test_bundle_zcml_registers_utility(self):
        self.layer.load_zcml_string('\n'.join((
                    '<configure xmlns:inflator="http://namespaces.zope.org/inflator"'
                    '           i18n_domain="my.package">',
                    '    <inflator:bundle',
                    '        title="foo"',
                    '        profiles="plonetheme.sunburst:default" />',
                    '</configure>'
                    )))

        utilites = self.get_utilites()
        self.assertEquals(len(utilites), 1)

        name, obj = utilites[0]
        self.assertEquals(name, u'foo')
        self.assertEquals(obj.title, u'foo')

    def test_title_and_description_translated(self):
        self.layer.load_zcml_string('\n'.join((
                    '<configure xmlns:inflator="http://namespaces.zope.org/inflator"'
                    '           i18n_domain="my.package">',
                    '    <inflator:bundle',
                    '        title="foo"',
                    '        description="bar"'
                    '        profiles="plonetheme.sunburst:default" />',
                    '</configure>'
                    )))

        utilites = self.get_utilites()
        self.assertEquals(len(utilites), 1)
        _name, obj = utilites[0]

        self.assertEquals(obj.title, u'foo')
        self.assertEquals(obj.title.default, None)
        self.assertEquals(type(obj.title).__name__, 'Message')
        self.assertEquals(obj.title.domain, 'my.package')

        self.assertEquals(obj.description, u'bar')
        self.assertEquals(obj.description.default, None)
        self.assertEquals(type(obj.description).__name__, 'Message')
        self.assertEquals(obj.description.domain, 'my.package')

    def test_profiles_is_list(self):
        self.layer.load_zcml_string('\n'.join((
                    '<configure xmlns:inflator="http://namespaces.zope.org/inflator"'
                    '           i18n_domain="my.package">',
                    '    <inflator:bundle',
                    '        title="foo"',
                    '        profiles="plonetheme.sunburst:default    ',
                    '                  Products.CMFPlone:plone-content  my.package:default" />',
                    '</configure>'
                    )))

        utilites = self.get_utilites()
        self.assertEquals(len(utilites), 1)
        _name, obj = utilites[0]

        self.assertEquals(obj.profiles, [u'plonetheme.sunburst:default',
                                         u'Products.CMFPlone:plone-content',
                                         u'my.package:default'])

    def test_defaults(self):
        self.layer.load_zcml_string('\n'.join((
                    '<configure xmlns:inflator="http://namespaces.zope.org/inflator"'
                    '           i18n_domain="my.package">',
                    '    <inflator:bundle',
                    '        title="foo"',
                    '        profiles="plonetheme.sunburst:default" />',
                    '</configure>'
                    )))

        utilites = self.get_utilites()
        self.assertEquals(len(utilites), 1)
        _name, obj = utilites[0]

        self.assertEqual(obj.title, u'foo')
        self.assertEqual(obj.profiles, [u'plonetheme.sunburst:default'])
        self.assertEqual(obj.description, u'')
        self.assertEqual(obj.base, _DEFAULT_PROFILE)
        self.assertEqual(obj.standard, False)

    def test_multiple_bundles(self):
        self.layer.load_zcml_string('\n'.join((
                    '<configure xmlns:inflator="http://namespaces.zope.org/inflator"'
                    '           i18n_domain="my.package">',

                    '    <inflator:bundle',
                    '        title="foo"',
                    '        profiles="plonetheme.sunburst:default" />',

                    '    <inflator:bundle',
                    '        title="bar"',
                    '        profiles="plonetheme.sunburst:default" />',

                    '</configure>'
                    )))

        utilites = self.get_utilites()
        self.assertEquals(len(utilites), 2)
        _name, foo = utilites[0]
        _name, bar = utilites[1]

        self.assertEquals(foo.title, u'foo')
        self.assertEquals(bar.title, u'bar')

    def test_reregistering_bundles(self):
        with self.assertRaises(ConfigurationConflictError):
            self.layer.load_zcml_string(
                '\n'.join((
                        '<configure xmlns:inflator="http://namespaces.zope.org/inflator"'
                        '           i18n_domain="my.package">',

                        '    <inflator:bundle',
                        '        title="foo"',
                        '        profiles="plonetheme.sunburst:default" />',

                        '    <inflator:bundle',
                        '        title="foo"',
                        '        profiles="plonetheme.sunburst:default" />',

                        '</configure>'
                        )))
