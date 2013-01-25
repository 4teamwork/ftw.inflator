from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from ftw.inflator.creation.sections import jsonsource
from unittest2 import TestCase
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject
import ftw.inflator.tests
import os.path


class TestRecursiveEncode(TestCase):

    def equals(self, input, output):
        self.assertEqual(jsonsource.recursive_encode(input), output)

    def test_unicode(self):
        self.equals(u'foo', 'foo')
        self.equals(u'b\xe4r', 'b\xc3\xa4r')
        self.equals('b\xc3\xa4r', 'b\xc3\xa4r')

    def test_dicts(self):
        self.equals({u'b\xe4r': u'b\xe4r'},
                    {'b\xc3\xa4r': 'b\xc3\xa4r'})

    def test_lists(self):
        self.equals([u'b\xe4r'], ['b\xc3\xa4r'])

    def test_other_types(self):
        self.equals([1, 2.2, True, False, None],
                    [1, 2.2, True, False, None])

        self.equals(1, 1)
        self.equals(None, None)

    def test_nesting(self):
        input = {
            u'b\xe4r': {
                u'b\xe4r': [
                    u'b\xe4r',
                    1,
                    True]},
            'blubb': [{
                    u'b\xe4r': 3}]}

        output = {
            'b\xc3\xa4r': {
                'b\xc3\xa4r': [
                    'b\xc3\xa4r',
                    1,
                    True]},
            'blubb': [{
                    'b\xc3\xa4r': 3}]}

        self.equals(input, output)


class TestJSONSource(TestCase):

    def test_implements_interface(self):
        klass = jsonsource.JSONSource

        self.assertTrue(ISection.implementedBy(klass),
                        'Class %s does not implement ISection.' % str(klass))
        verifyClass(ISection, klass)

        self.assertTrue(ISectionBlueprint.providedBy(klass),
                        'Class %s does not provide ISectionBlueprint.' % (
                str(klass)))
        verifyObject(ISectionBlueprint, klass)

    def test_directory_checks(self):
        existing_dir = os.path.dirname(jsonsource.__file__)
        missing_dir = os.path.join(existing_dir, 'foo-missing-dir')

        self.assertFalse(
            os.path.isdir(missing_dir),
            'Test not possible since unexpected directory present at %s' % (
                missing_dir))

        jsonsource.JSONSource(None, '', {'directory': existing_dir}, [])

        with self.assertRaises(IOError) as cm:
            jsonsource.JSONSource(None, '', {'directory': missing_dir}, [])

        self.assertEqual(str(cm.exception),
                         'Directory does not exists: %s' % missing_dir)

    def test_reiters_previous(self):
        directory = os.path.dirname(ftw.inflator.tests.__file__)

        source = jsonsource.JSONSource(
            None, '', {'directory': directory}, ['foo', 'bar'])

        self.assertEqual(list(source), ['foo', 'bar'])

    def test_json_file_parsing(self):
        directory = os.path.join(
            os.path.dirname(ftw.inflator.tests.__file__),
            'jsonsource')

        source = jsonsource.JSONSource(
            None, '', {'directory': directory}, ['previous'])

        self.assertEqual(list(source), ['previous', 'foo', 1, 'b\xc3\xa4r'])
