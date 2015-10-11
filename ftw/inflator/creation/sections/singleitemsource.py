from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from ftw.inflator.creation.sections.utils import recursive_encode
from zope.interface import classProvides
from zope.interface import implements


class SingleItemSource(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.options = options

    def __iter__(self):
        for item in self.previous:
            yield item

        yield recursive_encode(self.options['item'])
