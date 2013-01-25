from Products.ATContentTypes.lib import constraintypes
from Products.CMFPlone.utils import base_hasattr
from collective.transmogrifier.interfaces import ISectionBlueprint
from ftw.inflator.creation.sections.base import ObjectUpdater
from zope.interface import classProvides


class ConstraintypesUpdater(ObjectUpdater):
    classProvides(ISectionBlueprint)

    key_option_name = 'constraintypes-key'
    default_key_name = 'constrain_types'

    def update(self, obj, data):
        if base_hasattr(obj, 'getConstrainTypesMode'):
            obj.setConstrainTypesMode(constraintypes.ENABLED)

            immediately = tuple(data['immediately'])
            obj.setImmediatelyAddableTypes(immediately)

            locally = tuple(data['locally'])
            obj.setLocallyAllowedTypes(locally)
