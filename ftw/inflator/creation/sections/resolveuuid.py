from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from ftw.inflator.creation.sections.resolvepath import ResolvePath
from plone.uuid.interfaces import IUUID
from zope.interface import classProvides
from zope.interface import implements


class ResolveUUID(ResolvePath):

    PREFIX = 'resolveUUID::'

    classProvides(ISectionBlueprint)
    implements(ISection)

    def _resolve(self, item, value):
        obj = super(ResolveUUID, self)._resolve(item, value)
        return IUUID(obj)
