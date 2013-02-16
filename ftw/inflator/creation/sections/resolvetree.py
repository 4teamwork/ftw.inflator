from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from zope.interface import classProvides
from zope.interface import implements


class ResolveTree(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous

    def __iter__(self):
        for item in self.previous:
            for node in self._resolve(item):
                yield node

    def _resolve(self, item):
        children = []
        if '_children' in item:
            children = item['_children']
            del item['_children']

        yield item

        for child in children:
            child['_path'] = '/'.join((item['_path'].rstrip('/'),
                                       child['_id']))
            del child['_id']

            for node in self._resolve(child):
                yield node
