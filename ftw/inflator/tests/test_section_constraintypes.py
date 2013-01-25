from Products.CMFPlone.utils import base_hasattr
from ftw.inflator.creation.sections import constraintypes
from ftw.testing import MockTestCase


class TestConstraintypesUpdater(MockTestCase):

    def setUp(self):
        super(TestConstraintypesUpdater, self).setUp()
        transmogrifier = self.create_dummy(context=None)
        options = {'blueprint': ''}
        self.updater = constraintypes.ConstraintypesUpdater(
            transmogrifier, '', options, [])

    def test_nothing_done_when_no_constrain_support(self):
        obj = self.create_dummy()
        self.assertFalse(base_hasattr(obj, 'getConstrainTypesMode'))

    def test_set_constrain_types(self):
        obj = self.mocker.mock()
        self.expect(base_hasattr(obj, 'getConstrainTypesMode')).result(True)
        self.expect(obj.setConstrainTypesMode(1))
        self.expect(obj.setImmediatelyAddableTypes(('Folder',)))
        self.expect(obj.setLocallyAllowedTypes(('Folder', 'Page')))
        self.replay()

        data = {'locally': ['Folder', 'Page'],
                'immediately': ['Folder']}
        self.updater.update(obj, data)
