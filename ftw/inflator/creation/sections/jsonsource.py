from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import resolvePackageReferenceOrFile
from zope.interface import classProvides
from zope.interface import implements
import json
import os.path


def recursive_encode(data):
    """Encodes unicodes (from json) to utf-8 strings recursively.
    """
    if isinstance(data, unicode):
        return data.encode('utf-8')

    elif isinstance(data, str):
        return data

    elif isinstance(data, dict):
        for key, value in data.items():
            del data[key]
            data[recursive_encode(key)] = recursive_encode(value)
        return data

    elif isinstance(data, list):
        new_data = []
        for item in data:
            new_data.append(recursive_encode(item))
        return new_data

    elif hasattr(data, '__iter__'):
        for item in data:
            recursive_encode(item)
        return data

    else:
        return data


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

        for name in sorted(os.listdir(self.path)):
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
