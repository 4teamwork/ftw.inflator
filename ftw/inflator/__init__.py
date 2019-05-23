from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('ftw.inflator')


IS_PLONE_5 = get_distribution('Plone').version >= '5'

HAS_MULTILINGUAL = False
IS_PLONE_APP_MULTILINGUAL_2 = False

try:
    dist = get_distribution('plone.app.multilingual')
    IS_PLONE_APP_MULTILINGUAL_2 = '2' <= dist.version < '3'
    HAS_MULTILINGUAL = True
except DistributionNotFound:
    pass
