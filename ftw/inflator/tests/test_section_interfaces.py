from ftw.inflator.creation.sections import interfaces
from ftw.inflator.tests.interfaces import IFoo
from ftw.testing import MockTestCase
from zope.interface import alsoProvides


class TestInterfacesUpdater(MockTestCase):

    def setUp(self):
        super(TestInterfacesUpdater, self).setUp()
        transmogrifier = self.create_dummy(context=None)
        options = {'blueprint': ''}
        self.updater = interfaces.InterfacesUpdater(
            transmogrifier, '', options, [])

    def test_interface_also_provided(self):
        obj = self.create_dummy()
        self.assertFalse(IFoo.providedBy(obj))

        data = ['ftw.inflator.tests.interfaces.IFoo']
        self.updater.update(obj, data)
        self.assertTrue(IFoo.providedBy(obj))

    def test_interface_not_reprovided(self):
        obj = self.providing_stub([IFoo])
        self.replay()

        data = ['ftw.inflator.tests.interfaces.IFoo']
        self.updater.update(obj, data)

    def test_remove_interface(self):
        obj = self.create_dummy()
        alsoProvides(obj, IFoo)
        self.assertTrue(IFoo.providedBy(obj))

        data = ['remove:ftw.inflator.tests.interfaces.IFoo']
        self.updater.update(obj, data)
        self.assertFalse(IFoo.providedBy(obj))
