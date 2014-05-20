from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import defaultMatcher
from zope.interface import classProvides
from zope.interface import implements


class BlockLocalRoleInheritance(object):
    """Block the inheritance of ac_local_roles.
    """

    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context
        self.pathkey = defaultMatcher(options, 'path-key', name, 'path')
        self.block_local_roles_key = defaultMatcher(options,
                                                    'block-local-roles-key',
                                                    name,
                                                    'block-local-roles')

    def __iter__(self):
        for item in self.previous:
            self.set_block_local_roles(item)
            yield item

    def get_item_value(self, item, key):
        return item.get(key(*item.keys())[0], None)

    def set_block_local_roles(self, item):
        path = self.get_item_value(item, self.pathkey)
        if not path:
            return

        obj = self.context.unrestrictedTraverse(path.lstrip('/'), None)
        if not obj:
            return

        block_local_roles = self.get_item_value(item,
                                                self.block_local_roles_key)
        if not block_local_roles:
            return

        obj.__ac_local_roles_block__ = True
        obj.reindexObjectSecurity()
