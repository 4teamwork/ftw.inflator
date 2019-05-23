from collective.transmogrifier.interfaces import ISectionBlueprint
from ftw.inflator import IS_PLONE_5
from ftw.inflator import IS_PLONE_APP_MULTILINGUAL_2
from ftw.inflator.creation.sections.base import ObjectUpdater
from Products.CMFPlone.utils import base_hasattr
from zope.interface import classProvides


if IS_PLONE_5 or IS_PLONE_APP_MULTILINGUAL_2:
    from plone.app.dexterity.behaviors import constrains as constraintypes
    from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
else:
    from Products.ATContentTypes.lib import constraintypes


class ConstraintypesUpdater(ObjectUpdater):
    classProvides(ISectionBlueprint)

    key_option_name = 'constraintypes-key'
    default_key_name = 'constrain_types'

    def update(self, obj, data):
        if IS_PLONE_5 or IS_PLONE_APP_MULTILINGUAL_2:
            constrains = ISelectableConstrainTypes(obj)
            if constrains:
                constrains.setConstrainTypesMode(constraintypes.ENABLED)

                immediately = tuple(data['immediately'])
                constrains.setImmediatelyAddableTypes(immediately)

                locally = tuple(data['locally'])
                constrains.setLocallyAllowedTypes(locally)

        else:
            if base_hasattr(obj, 'getConstrainTypesMode'):
                obj.setConstrainTypesMode(constraintypes.ENABLED)

                immediately = tuple(data['immediately'])
                obj.setImmediatelyAddableTypes(immediately)

                locally = tuple(data['locally'])
                obj.setLocallyAllowedTypes(locally)
