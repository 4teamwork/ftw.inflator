from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.utils import defaultMatcher
from zope.interface import implements


class ObjectUpdater(object):

    implements(ISection)

    key_option_name = None
    default_key_name = None

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context
        self.datakey = defaultMatcher(
            options, self.key_option_name, name, self.default_key_name)
        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')

    def __iter__(self):
        for item in self.previous:
            data = item.get(self.datakey(*item.keys())[0], None)
            obj = self._get_obj(item)
            if obj and data:
                self.update(obj, data)

            yield item

    def _get_obj(self, item):
        path = item.get(self.pathkey(*item.keys())[0], None)
        # Skip the Plone site object itself
        if not path:
            return None

        obj = self.context.unrestrictedTraverse(
            path.encode('utf-8').lstrip('/'), None)

        return obj

    def update(self, obj, data):
        raise NotImplementedError()
