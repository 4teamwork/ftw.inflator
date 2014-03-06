from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from ftw.inflator.creation.sections import resolvetree
from unittest2 import TestCase
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject


class TestResolveTreeBlueprint(TestCase):

    def test_implements_interface(self):
        klass = resolvetree.ResolveTree

        self.assertTrue(ISection.implementedBy(klass),
                        'Class %s does not implement ISection.' % str(klass))
        verifyClass(ISection, klass)

        self.assertTrue(ISectionBlueprint.providedBy(klass),
                        'Class %s does not provide ISectionBlueprint.' %
                        str(klass))
        verifyObject(ISectionBlueprint, klass)

    def test_resolves_tree_structure(self):
        input = [{
            '_path': 'foo',
            '_children': [{
                '_id': 'bar',
                'title': 'Bar',
                '_children': [{
                    '_id': 'baz'}]
            }, {
                '_path': '/qux/there',
                'title': 'Something'
            }]
        }]

        expected = [
            {'_path': 'foo'},
            {'_path': 'foo/bar',
             'title': 'Bar'},
            {'_path': 'foo/bar/baz'},
            {'_path': 'foo/qux/there',
             'title': 'Something'}
        ]

        source = resolvetree.ResolveTree(None, '', None, input)
        output = list(source)

        self.maxDiff = None
        self.assertEqual(output, expected)
