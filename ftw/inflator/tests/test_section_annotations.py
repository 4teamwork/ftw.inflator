from ftw.inflator.creation.sections import annotations
from ftw.testing import MockTestCase
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping
from zope.annotation.attribute import AttributeAnnotations
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.component import provideAdapter
from zope.interface import alsoProvides


class TestAnnotationsUpdater(MockTestCase):

    def setUp(self):
        super(TestAnnotationsUpdater, self).setUp()
        transmogrifier = self.create_dummy(context=None)
        options = {'blueprint': ''}
        self.updater = annotations.AnnotationsUpdater(
            transmogrifier, '', options, [])

        provideAdapter(AttributeAnnotations,
                       adapts=(IAttributeAnnotatable,))

    def test_simple_annotation(self):
        obj = self.create_dummy()
        alsoProvides(obj, IAttributeAnnotatable)

        data = {'foo': 'bar'}
        self.updater.update(obj, data)

        self.assertEquals(IAnnotations(obj).get('foo'), 'bar')

    def test_simple_persistent_mapping(self):
        obj = self.create_dummy()
        alsoProvides(obj, IAttributeAnnotatable)

        data = {'foo': {'bar': 'baz'}}
        self.updater.update(obj, data)

        foo = IAnnotations(obj).get('foo')
        self.assertTrue(isinstance(foo, PersistentMapping))

    def test_simple_persistent_list(self):
        obj = self.create_dummy()
        alsoProvides(obj, IAttributeAnnotatable)

        data = {'foo': ['bar', 'baz']}
        self.updater.update(obj, data)

        foo = IAnnotations(obj).get('foo')
        self.assertTrue(isinstance(foo, PersistentList))

    def test_nested_persistent_mapping(self):
        obj = self.create_dummy()
        alsoProvides(obj, IAttributeAnnotatable)

        data = {'foo': {'bar': {'baz': 'baz'}}}
        self.updater.update(obj, data)

        foo = IAnnotations(obj).get('foo')
        bar = foo.get('bar')
        self.assertTrue(isinstance(bar, PersistentMapping))

    def test_nested_persistent_list(self):
        obj = self.create_dummy()
        alsoProvides(obj, IAttributeAnnotatable)

        data = {'foo': [['bar', 'baz']]}
        self.updater.update(obj, data)

        foo = IAnnotations(obj).get('foo')
        bar = foo[0]
        self.assertTrue(isinstance(bar, PersistentList))
