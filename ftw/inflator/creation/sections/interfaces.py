from collective.transmogrifier.interfaces import ISectionBlueprint
from ftw.inflator.creation.sections.base import ObjectUpdater
from zope.dottedname.resolve import resolve
from zope.interface import alsoProvides
from zope.interface import classProvides


class InterfacesUpdater(ObjectUpdater):
    classProvides(ISectionBlueprint)

    key_option_name = 'interfaces-key'
    default_key_name = 'interfaces'

    def update(self, obj, interfaces):
        for iface in interfaces:
            iface = iface.encode('utf-8')
            resolved_iface = resolve(iface)

            if not resolved_iface.providedBy(obj):
                alsoProvides(obj, resolved_iface)
