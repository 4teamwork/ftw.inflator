from ftw.inflator.creation.sections import schemaupdater
from ftw.testing import MockTestCase


class ArchetypesFTI(object):
    pass


class DexterityFTI(object):
    pass


class TestNoDexteritySupportUpdateSection(MockTestCase):

    def setUp(self):
        super(TestNoDexteritySupportUpdateSection, self).setUp()
        self.transmogrifier = self.create_dummy(context=None)

    def test_yields_non_dexterity_types(self):
        portal_types = self.stub()
        fti = ArchetypesFTI()
        self.expect(portal_types.get('SomeType')).result(fti)
        self.mock_tool(portal_types, 'portal_types')
        self.replay()

        item = {'_type': 'SomeType'}
        updater = schemaupdater.NoDexteritySupportUpdateSection(
            self.transmogrifier, '', {}, [item])

        self.assertEqual(list(updater), [item])

    def test_raises_on_dexterity_types(self):
        portal_types = self.stub()
        fti = DexterityFTI()
        self.expect(portal_types.get('OtherType')).result(fti)
        self.mock_tool(portal_types, 'portal_types')
        self.replay()

        item = {'_type': 'OtherType'}
        updater = schemaupdater.NoDexteritySupportUpdateSection(
            self.transmogrifier, '', {}, [item])

        with self.assertRaises(ValueError) as cm:
            list(updater)

        self.assertEqual(
            str(cm.exception),
            'Trying to update a dexterity object of type OtherType but'
            ' transmogrify.dexterity is not installed'
            " ({'_type': 'OtherType'})")
