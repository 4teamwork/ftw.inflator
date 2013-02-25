from Products.CMFCore.utils import getToolByName
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from zope.interface import classProvides
from zope.interface import implements
import pkg_resources


try:
    pkg_resources.get_distribution('transmogrify.dexterity')

except pkg_resources.DistributionNotFound:
    DEXTERITY_SUPPORT = False

else:
    from transmogrify.dexterity.schemaupdater import DexterityUpdateSection
    DEXTERITY_SUPPORT = True


class NoDexteritySupportUpdateSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.context = transmogrifier.context
        self.previous = previous

    def __iter__(self):
        ttool = getToolByName(self.context, 'portal_types')

        for item in self.previous:
            fti = ttool.get(item.get('_type'))
            if fti and fti.__class__.__name__ == 'DexterityFTI':
                raise ValueError('Trying to update a dexterity object of'
                                 ' type %s but transmogrify.dexterity is'
                                 ' not installed (%s)' % (
                        item.get('_type'),
                        str(item)))

            yield item


if DEXTERITY_SUPPORT:
    DxUpdateSection = DexterityUpdateSection
else:
    DxUpdateSection = NoDexteritySupportUpdateSection
