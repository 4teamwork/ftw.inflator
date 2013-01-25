from Products.CMFCore.utils import getToolByName
from collective.transmogrifier.interfaces import ISectionBlueprint
from ftw.inflator.creation.sections.base import ObjectUpdater
from zope.interface import classProvides


class PlacefulworkflowUpdater(ObjectUpdater):
    """Placeful workflow updater section, activating a placeful workflow
    policy.

    Example:
    {
        "_path": "foo/intranet",
        "_type": "Folder",
        "title": "Intranet",
        "_placefulworkflow": ["one-state", "intranet"]
    }

    This activates the placeful workflow policy "one-state" for the
    "intranet" object, but the "intranet" workflow policy for children.
    """

    classProvides(ISectionBlueprint)

    key_option_name = 'placefulworkflow-key'
    default_key_name = 'placefulworkflow'

    def update(self, obj, data):
        policy_in, policy_below = data

        placeful_workflow = getToolByName(obj, 'portal_placeful_workflow')
        config = placeful_workflow.getWorkflowPolicyConfig(obj)

        if not config:
            obj.manage_addProduct[
                'CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
            config = placeful_workflow.getWorkflowPolicyConfig(obj)

        config.setPolicyIn(policy=policy_in)
        config.setPolicyBelow(policy=policy_below, update_security=True)
