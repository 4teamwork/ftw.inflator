from collective.transmogrifier.transmogrifier import Transmogrifier
from ftw.inflator.testing import INFLATOR_INTEGRATION_TESTING
from unittest2 import TestCase


class TestSingleItemContentCreation(TestCase):
    layer = INFLATOR_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_create_single_item(self):
        item = {'_path': 'foo',
                '_type': 'Folder',
                'title': 'Foo'}

        mogrifier = Transmogrifier(self.portal)
        self.assertNotIn('foo', self.portal)
        mogrifier(u'ftw.inflator.creation.single_item_content_creation',
                  jsonsource=dict(item=item))
        self.assertIn('foo', self.portal)
        self.assertEquals('Foo', self.portal.foo.Title())
