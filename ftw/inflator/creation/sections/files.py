from OFS.Image import File
from Products.CMFCore.utils import getToolByName
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
        self.ttool = getToolByName(self.context, 'portal_types')

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

        filename_key = '{}:filename'.format(fieldname)
        if filename_key in item:
            filename = item[filename_key]
        else:
            filename = os.path.basename(path)

        file_ = open(path, 'rb')
        try:
            fti = self.ttool.get(item.get('_type'))
            if fti and fti.__class__.__name__ == 'DexterityFTI':
                self.add_dx_file(item, fieldname, filename, file_)
            else:
                self.add_at_file(item, fieldname, filename, file_)
        finally:
            file_.close()

    def add_dx_file(self, item, fieldname, filename, file_):
        item[fieldname] = file_.read()
        # surprisingly this does not have a filename prefix/postfix so it
        # might only work with one file.
        item['_filename'] = filename

    def add_at_file(self, item, fieldname, filename, file_):
        item[fieldname] = File(filename, filename, file_)
        setattr(item[fieldname], 'filename', filename)
