from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from ftw.inflator.creation.sections import translate
from ftw.inflator.testing import ZCML
from ftw.testing import MockTestCase
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject


class TestTranslateBlueprint(MockTestCase):

    layer = ZCML

    def test_implements_interface(self):
        klass = translate.Translate

        self.assertTrue(ISection.implementedBy(klass),
                        'Class %s does not implement ISection.' % str(klass))
        verifyClass(ISection, klass)

        self.assertTrue(ISectionBlueprint.providedBy(klass),
                        'Class %s does not provide ISectionBlueprint.' % (
                str(klass)))
        verifyObject(ISectionBlueprint, klass)

    def test_translates(self):
        transmogrifier = self.stub()
        self.expect(transmogrifier.context.Language()).result('en')
        self.replay()

        input = [
            {'_id:translate(ftw.inflator.tests)': 'intranet-id',
             'title:translate(ftw.inflator.tests)': 'intranet-title',
             'foo': [{'title:translate(ftw.inflator.tests)': 'intranet-title'}]}]

        expected = [
            {'_id': u'intranet',
             'title': u'Intranet',
             'foo': [{'title': u'Intranet'}]}]

        source = translate.Translate(transmogrifier, '', None, input)
        output = list(source)

        self.maxDiff = None
        self.assertEqual(output, expected)

    def test_translates_encoding(self):
        transmogrifier = self.stub()
        self.expect(transmogrifier.context.Language()).result('en')
        self.replay()

        # UTF-8 encoded value for the title.
        input = [
            {'_id:translate(ftw.inflator.tests)': 'burger',
             'title:translate(ftw.inflator.tests)': 'B\xc3\xbcrger'}]

        expected = [
            {'_id': u'burger',
             'title': u'B\xfcrger'}]

        source = translate.Translate(transmogrifier, '', None, input)
        output = list(source)

        self.maxDiff = None
        self.assertEqual(output, expected)
