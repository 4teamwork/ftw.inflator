from pkg_resources import get_distribution
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('ftw.inflator')


IS_PLONE_5 = get_distribution('Plone').version >= '5'
