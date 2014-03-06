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
            child_path = None
            if '_id' in child:
                child_path = child.pop('_id')
            elif '_path' in child:
                child_path = child.pop('_path').strip('/')

            assert child_path, 'child _id or _path must be specified'
            child['_path'] = '/'.join((item['_path'].rstrip('/'),
                                       child_path))

            for node in self._resolve(child):
                yield node
