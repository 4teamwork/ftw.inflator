from collective.transmogrifier.interfaces import ISectionBlueprint
from ftw.inflator.creation.sections.base import ObjectUpdater
from zope.interface import classProvides


class PropertiesUpdater(ObjectUpdater):
    classProvides(ISectionBlueprint)

    key_option_name = 'properties-key'
    default_key_name = 'properties'

    def update(self, obj, properties):
        for key, data in properties.items():
            type_, value = data

            if obj.getProperty(key):
                obj._updateProperty(key, value)
            else:
                obj._setProperty(key, value, type_)
