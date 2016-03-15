from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import resolvePackageReferenceOrFile
from ftw.inflator.creation.progresslogger import ProgressLogger
from ftw.inflator.creation.sections.utils import recursive_encode
from zope.interface import classProvides
from zope.interface import implements
import json
import os.path


class JSONSource(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous

        self.path = resolvePackageReferenceOrFile(options['directory'])
        if self.path is None or not os.path.isdir(self.path):
            raise IOError('Directory does not exists: %s' % self.path)

    def __iter__(self):
        for item in self.previous:
            yield item

        msg = 'Importing content_creation files with inflator.'
        for name in ProgressLogger(msg, sorted(os.listdir(self.path))):
            if name.startswith('.') or not name.endswith('.json'):
                continue

            path = os.path.join(self.path, name)
            if not os.path.isfile(path):
                continue

            locals()['__traceback_info__'] = path

            with open(path) as file_:
                data = json.loads(file_.read())

            for item in data:
                # yield item
                yield recursive_encode(item)
