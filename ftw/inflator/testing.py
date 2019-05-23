from collective.transmogrifier import transmogrifier
from ftw.inflator import IS_PLONE_APP_MULTILINGUAL_2
from ftw.inflator.patches import apply_patches
from ftw.testing import ComponentRegistryLayer
from ftw.testing import IS_PLONE_5
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
from plone.app.testing.layers import PloneFixture
from plone.testing import z2
from Testing.ZopeTestCase.utils import setupCoreSessions
from zope.configuration import xmlconfig


def clear_transmogrifier_registry():
    # pylint: disable=W0212
    transmogrifier.configuration_registry._config_info = {}
    transmogrifier.configuration_registry._config_ids = []
    # pylint: enable=W0212


class MetaZCMLLayer(ComponentRegistryLayer):

    def setUp(self):
        super(MetaZCMLLayer, self).setUp()

        import ftw.inflator
        self.load_zcml_file('meta.zcml', ftw.inflator)


META_ZCML = MetaZCMLLayer()


class ZCMLLayer(ComponentRegistryLayer):

    def setUp(self):
        super(ZCMLLayer, self).setUp()

        import ftw.inflator.tests
        self.load_zcml_file('configure.zcml', ftw.inflator.tests)


ZCML = ZCMLLayer()


class ZopeLayer(PloneFixture):
    # we use the PloneFixture but do not create the plone site.

    defaultBases = (z2.STARTUP, )

    def setUpProducts(self, app):
        super(ZopeLayer, self).setUpProducts(app)
        configurationContext = self['configurationContext']

        # Plone < 4.3
        import Products.GenericSetup
        xmlconfig.file('meta.zcml', Products.GenericSetup,
                       context=configurationContext)

        import Products.CMFPlacefulWorkflow
        xmlconfig.file('configure.zcml', Products.CMFPlacefulWorkflow,
                       context=configurationContext)

        if IS_PLONE_5:
            xmlconfig.string('''
            <configure>
            <include package="plone.app.caching" />
            <include package="plonetheme.barceloneta" />
            </configure>''', context=configurationContext)

        z2.installProduct(app, 'Products.CMFPlacefulWorkflow')

        import Products.Five
        xmlconfig.file('meta.zcml', Products.Five,
                       context=configurationContext)

        import ftw.inflator
        xmlconfig.file('configure.zcml', ftw.inflator,
                       context=configurationContext)
        xmlconfig.file('overrides.zcml', ftw.inflator,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', ftw.inflator.tests,
                       context=configurationContext)

        apply_patches()

    def setUpDefaultContent(self, app):
        # do not create plone site
        with z2.zopeApp() as app:
            app['acl_users'].userFolderAddUser(
                    SITE_OWNER_NAME,
                    SITE_OWNER_PASSWORD,
                    ['Manager'],
                    []
                )

    def tearDown(self):
        super(ZopeLayer, self).tearDown()
        clear_transmogrifier_registry()


ZOPE_LAYER = ZopeLayer()
ZOPE_FUNCTIONAL_TESTING = z2.FunctionalTesting(
    bases=(ZOPE_LAYER, ),
    name='ftw.inflator:ZOPE_FUNCTIONAL_TESTING')


class InflatorLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import Products.CMFPlacefulWorkflow
        xmlconfig.file('configure.zcml', Products.CMFPlacefulWorkflow,
                       context=configurationContext)

        z2.installProduct(app, 'Products.CMFPlacefulWorkflow')

        if IS_PLONE_APP_MULTILINGUAL_2:
            z2.installProduct(app, 'Products.DateRecurringIndex')

        import ftw.inflator
        xmlconfig.file('configure.zcml', ftw.inflator,
                       context=configurationContext)

        xmlconfig.file('configure.zcml', ftw.inflator.tests,
                       context=configurationContext)

        import plone.app.multilingual
        xmlconfig.file('configure.zcml', plone.app.multilingual,
                       context=configurationContext)

        import plone.app.dexterity
        xmlconfig.file('configure.zcml', plone.app.dexterity,
                       context=configurationContext)

        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

        setupCoreSessions(app)

    def setUpPloneSite(self, portal):
        if IS_PLONE_5 or IS_PLONE_APP_MULTILINGUAL_2:
            applyProfile(portal, 'plone.app.contenttypes:default')

        applyProfile(
            portal, 'Products.CMFPlacefulWorkflow:CMFPlacefulWorkflow')

    def tearDown(self):
        super(InflatorLayer, self).tearDown()
        clear_transmogrifier_registry()


INFLATOR_FIXTURE = InflatorLayer()
INFLATOR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(INFLATOR_FIXTURE, ), name="ftw.inflator:Integration")
INFLATOR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(INFLATOR_FIXTURE, ), name="ftw.inflator:Functional")
