from ftw.inflator.creation.sections import properties
from ftw.testing import MockTestCase


class TestPropertiesUpdater(MockTestCase):

    def setUp(self):
        super(TestPropertiesUpdater, self).setUp()
        transmogrifier = self.create_dummy(context=None)
        options = {'blueprint': ''}
        self.updater = properties.PropertiesUpdater(
            transmogrifier, '', options, [])

    def test_create_properties(self):
        obj = self.mocker.mock()
        self.expect(obj.getProperty('foo')).result(None)
        self.expect(obj._setProperty('foo', 'bar', 'string'))
        self.replay()

        data = {'foo': ['string', 'bar']}
        self.updater.update(obj, data)

    def test_update_properties(self):
        obj = self.mocker.mock()
        self.expect(obj.getProperty('foo')).result('something')
        self.expect(obj._updateProperty('foo', 'bar'))
        self.replay()

        data = {'foo': ['string', 'bar']}
        self.updater.update(obj, data)
