from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from ftw.inflator.creation.sections.base import ObjectUpdater
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.interfaces import IFactory
from zope.interface import classProvides
from zope.interface import implements


class PortletUpdater(ObjectUpdater):
    """Add or replace portlets for a given context."""

    classProvides(ISectionBlueprint)
    implements(ISection)

    key_option_name = 'portlets-key'
    default_key_name = 'portlets'

    def update(self, obj, data):
        for key, conf in data.items():
            manager = getUtility(IPortletManager, key)
            mapping = getMultiAdapter(
                (obj, manager), IPortletAssignmentMapping)

            for portlet in conf.get('assignments', []):
                self.create_assignment(portlet, mapping)

            if conf.get('blacklist_status'):
                self.set_blacklist(conf.get('blacklist_status'), obj, manager)

    def create_assignment(self, properties, mapping):
        portlet_id = properties.pop('id')
        portlet_type = properties.pop('portlet_type')

        portlet_factory = getUtility(IFactory, name=portlet_type)
        assignment = portlet_factory(**properties)
        mapping[portlet_id] = assignment

    def set_blacklist(self, configuration, obj, manager):
        assignable = getMultiAdapter((obj, manager),
                                     ILocalPortletAssignmentManager)

        for category, status in configuration.items():
            if status.lower() == 'block':
                assignable.setBlacklistStatus(category, True)
            elif status.lower() == 'show':
                assignable.setBlacklistStatus(category, False)
            elif status.lower() == 'acquire':
                assignable.setBlacklistStatus(category, None)
            else:
                raise ValueError(
                    'Invalid blacklist status {!r}'.format(status))
