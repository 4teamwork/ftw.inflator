from collective.transmogrifier.interfaces import ISectionBlueprint
from ftw.inflator.creation.sections.base import ObjectUpdater
from zope.dottedname.resolve import resolve
from zope.interface import alsoProvides
from zope.interface import classProvides
from zope.interface import noLongerProvides


class InterfacesUpdater(ObjectUpdater):
    classProvides(ISectionBlueprint)

    key_option_name = 'interfaces-key'
    default_key_name = 'interfaces'

    def update(self, obj, interfaces):
        for iface in interfaces:
            iface = iface.encode('utf-8')
            remove = False

            if iface.startswith('remove:'):
                remove = True
                iface = iface[len('remove:'):]

            resolved_iface = resolve(iface)

            if not remove and not resolved_iface.providedBy(obj):
                alsoProvides(obj, resolved_iface)

            elif remove and resolved_iface.providedBy(obj):
                noLongerProvides(obj, resolved_iface)
