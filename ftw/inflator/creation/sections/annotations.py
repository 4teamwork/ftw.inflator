from collective.transmogrifier.interfaces import ISectionBlueprint
from ftw.inflator.creation.sections.base import ObjectUpdater
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping
from zope.annotation.interfaces import IAnnotations
from zope.interface import classProvides


def make_persistent(data):
    if isinstance(data, dict):
        new = PersistentMapping()
        for key, value in data.items():
            new[make_persistent(key)] = make_persistent(value)
        return new

    elif isinstance(data, list):
        new = PersistentList()
        for value in data:
            new.append(make_persistent(value))
        return new

    else:
        return data


class AnnotationsUpdater(ObjectUpdater):
    classProvides(ISectionBlueprint)

    key_option_name = 'annotations-key'
    default_key_name = 'annotations'

    def update(self, obj, data):
        annotations = IAnnotations(obj)

        for key, value in data.items():
            annotations[make_persistent(key)] = make_persistent(value)
