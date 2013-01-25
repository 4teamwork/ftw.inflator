from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig


class InflatorLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import ftw.inflator
        xmlconfig.file('configure.zcml', ftw.inflator,
                       context=configurationContext)

        xmlconfig.file('configure.zcml', ftw.inflator.tests,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        pass


INFLATOR_FIXTURE = InflatorLayer()
INFLATOR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(INFLATOR_FIXTURE, ), name="ftw.inflator:Integration")
INFLATOR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(INFLATOR_FIXTURE, ), name="ftw.inflator:Functional")
