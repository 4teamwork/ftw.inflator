from OFS.Image import File
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from zope.interface import classProvides
from zope.interface import implements
import os


class FileInserter(object):

    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context

    def __iter__(self):
        for item in self.previous:
            for key in item.keys():
                if key.endswith(':file'):
                    self.load_file(item, key)

            yield item

    def load_file(self, item, key):
        fieldname = key[:-len(':file')]
        directory = self.transmogrifier.get('jsonsource').get('directory')
        path = os.path.join(directory, item.get(key))
        filename = os.path.basename(path)
        file_ = open(path, 'rb')
        item[fieldname] = File(filename, filename, file_)
        setattr(item[fieldname], 'filename', filename)
