from ftw.inflator.bundle import get_bundles
from ftw.inflator.testing import META_ZCML
from ftw.testing import MockTestCase


class TestBundlesZCML(MockTestCase):

    layer = META_ZCML

    def test_getting_bundles_with_no_bundles_registered(self):
        self.assertEquals(get_bundles(), [])

    def test_getting_bundles(self):
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

        bundles = get_bundles()
        self.assertEquals(type(bundles), list)
        self.assertEquals(len(bundles), 2)

        bar, foo = bundles

        self.assertEquals(foo.title, u'foo')
        self.assertEquals(bar.title, u'bar')

    def test_bundle_sorting(self):
        # 1. non-standard first, then standard
        # 2. sort by title

        self.layer.load_zcml_string('\n'.join((
                    '<configure xmlns:inflator="http://namespaces.zope.org/inflator"'
                    '           i18n_domain="my.package">',

                    '    <inflator:bundle',
                    '        title="foo-standard"',
                    '        profiles="plonetheme.sunburst:default"'
                    '        standard="True" />',

                    '    <inflator:bundle',
                    '        title="bar"',
                    '        profiles="plonetheme.sunburst:default" />',

                    '    <inflator:bundle',
                    '        title="foo"',
                    '        profiles="plonetheme.sunburst:default" />',

                    '    <inflator:bundle',
                    '        title="bar-standard"',
                    '        profiles="plonetheme.sunburst:default"'
                    '        standard="True" />',

                    '</configure>'
                    )))

        bundles = get_bundles()
        self.assertEquals(type(bundles), list)
        self.assertEquals(len(bundles), 4)

        ordered_titles = [bundle.title for bundle in bundles]
        self.assertEqual(ordered_titles,
                         [u'bar',
                          u'foo',
                          u'bar-standard',
                          u'foo-standard'])
