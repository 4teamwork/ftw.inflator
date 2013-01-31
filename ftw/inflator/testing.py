from ftw.testing import ComponentRegistryLayer
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2
from zope.configuration import xmlconfig


class MetaZCMLLayer(ComponentRegistryLayer):

    def setUp(self):
        super(MetaZCMLLayer, self).setUp()

        import ftw.inflator
        self.load_zcml_file('meta.zcml', ftw.inflator)


META_ZCML = MetaZCMLLayer()


class InflatorLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import Products.CMFPlacefulWorkflow
        xmlconfig.file('configure.zcml', Products.CMFPlacefulWorkflow,
                       context=configurationContext)

        z2.installProduct(app, 'Products.CMFPlacefulWorkflow')

        import ftw.inflator
        xmlconfig.file('configure.zcml', ftw.inflator,
                       context=configurationContext)

        xmlconfig.file('configure.zcml', ftw.inflator.tests,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(
            portal, 'Products.CMFPlacefulWorkflow:CMFPlacefulWorkflow')


INFLATOR_FIXTURE = InflatorLayer()
INFLATOR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(INFLATOR_FIXTURE, ), name="ftw.inflator:Integration")
INFLATOR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(INFLATOR_FIXTURE, ), name="ftw.inflator:Functional")
