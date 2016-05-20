import os
from setuptools import setup, find_packages


version = '1.8.0'


extras_require = {
    'dexterity': [
        'plone.app.dexterity',
        'transmogrify.dexterity',
        ],

    'multilingual': [
        'plone.app.multilingual',
        'plone.multilingualbehavior',  # both are required
        ]}


extras_require['tests'] = tests_require = [
    'unittest2',
    'ftw.testing',
    'zope.configuration',
    'plone.testing',
    'plone.app.testing',
    'Products.CMFPlacefulWorkflow',
    ] + reduce(list.__add__, extras_require.values())


setup(name='ftw.inflator',
      version=version,
      description='Plone site setup wizard with content creation and ' + \
          'bundle system for predefined configurations.',

      long_description=open('README.rst').read() + '\n' + \
          open(os.path.join('docs', 'HISTORY.txt')).read(),

      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw inflator',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.inflator',

      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', ],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',

        'zope.annotation',
        'zope.component',
        'zope.configuration',
        'zope.dottedname',
        'zope.i18n',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
        'ZODB3',
        'Zope2',

        'plone.i18n',
        'plone.uuid',
        'Products.ATContentTypes',
        'Products.CMFCore',
        'Products.CMFPlone',
        'Products.GenericSetup',

        'plone.app.transmogrifier',
        'collective.transmogrifier',
        'collective.blueprint.jsonmigrator',

        'ftw.profilehook',
        ],

      tests_require=tests_require,
      extras_require=extras_require,

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
