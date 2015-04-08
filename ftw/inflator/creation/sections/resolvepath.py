from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import defaultMatcher
from ftw.inflator.creation.sections.helpers import map_recursive
from zope.interface import classProvides
from zope.interface import implements


class ResolvePath(object):

    PREFIX = 'resolvePath::'

    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.context = transmogrifier.context
        self.previous = previous
        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')

    def __iter__(self):
        for item in self.previous:
            yield map_recursive(
                lambda value: value.startswith(self.PREFIX),
                lambda value: self._resolve(item, value),
                item)

    def _resolve(self, item, value):
        value = value.replace(self.PREFIX, '', 1)

        return self._get_object_by_path(item, value)

    def _get_object_by_path(self, item, path):
        if isinstance(path, unicode):
            path = path.encode('utf-8')

        path = path.rstrip('/')

        if path.startswith('/'):
            return self.context.unrestrictedTraverse(path.lstrip('/'))
        else:
            item_obj = self._get_obj(item)
            return item_obj.unrestrictedTraverse(path)

    def _get_obj(self, item):
        path = item.get(self.pathkey(*item.keys())[0], None)
        obj = self.context.unrestrictedTraverse(
            path.encode('utf-8').lstrip('/'), None)
        return obj
