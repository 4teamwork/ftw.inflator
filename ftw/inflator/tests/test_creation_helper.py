from unittest2 import TestCase
from ftw.inflator.creation.sections import helpers


class TestMapRecursiveValue(TestCase):

    def test_simple_list(self):
        data = ['foo', 'upper::bar', 'baz']
        result = helpers.map_recursive(
            lambda item: item.startswith('upper::'),
            lambda item: item.lstrip('upper::').upper(),
            data)

        self.assertEquals(result, ['foo', 'BAR', 'baz'])

    def test_simple_tuple(self):
        data = ('foo', 'upper::bar', 'baz')
        result = helpers.map_recursive(
            lambda item: item.startswith('upper::'),
            lambda item: item.lstrip('upper::').upper(),
            data)

        self.assertEquals(result, ('foo', 'BAR', 'baz'))

    def test_simple_dict(self):
        data = {'foo': 'upper::bar',
                'upper::baz': 5,
                'bar': 'bar'}

        result = helpers.map_recursive(
            lambda item: item.startswith('upper::'),
            lambda item: item.lstrip('upper::').upper(),
            data)

        self.assertEquals(result, {
                'foo': 'BAR',
                'BAZ': 5,
                'bar': 'bar'})

    def test_nested(self):
        data = ({'foo': ['bar', {'baz': 'upper::foo',
                                 'upper::foo': 2}]},
                3)

        result = helpers.map_recursive(
            lambda item: item.startswith('upper::'),
            lambda item: item.lstrip('upper::').upper(),
            data)

        self.assertEquals(result, (
                {'foo': ['bar', {'baz': 'FOO',
                                 'FOO': 2}]},
                3))
