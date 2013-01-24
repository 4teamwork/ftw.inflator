ftw.inflator
============

This packages helps predefining a Plone site setup including content
creation (using generic setup), defining multiple bundles and a wizard
for installing a new site with a bundle.

Features
--------

- A simplified site setup wizard. The wizard can be customized and branded.
- A bundle system for defining variants in the setup configuration.
- A generic setup site creation import step which can be used in the bundles
  for creating initial content. It can be used without using the setup wizard
  and bundle system.


Installation
------------

- Add ``ftw.inflator`` to your buildout configuration:

::

    [instance]
    eggs +=
        ftw.inflator


Setup wizard
------------

On the `manage_main` view of the Zope app there is an additional button
for installing your product.
It leads to the site setup wizard where an ID and a bundle can be selected.

Unlike the plone default setup wizard this wizard does not allow to select
the addons since the bundle system is meant to be used for a full already
configured product which.
The various bundles may install additional addons.

**TODO**: Add a screenshot.

**TODO**: Document how to configure the product-title and -logo.


Bundle system
-------------

A bundle defines a list of profiles which are automatically applied when
creating a new Plone site with this bundle.

*Defining bundles*

Add a list of bundles to the ``__init__.py`` of your package, e.g. at
``my/package/__init__.py``::


    BUNDLES = [
        {'title': 'my.package: unthemed',
         'description': 'Install the my.package product without '
                        'installing the default theme.',
         'profiles': [
                'my.package:default',
                ]},

        {'title': 'my.package: themed',
         'description': 'Install the my.package product with the'
                        'default theme.',
         'profiles': [
                'my.package:default',
                'my.package:theme',
                ]}]


**TODO**: Document base profile and standard profile options.

*Registering the bundles*

Registering the bundles list is done by defining an entry-point in the
``setup.py``, pointing to a module with a variable ``BUNDLES`` containing
the bundles list::

    from setuptools import setup
    setup(name='my.package',
          entry_points="""
          [ftw.inflator]
          bundles = my.package
          """,
          )


Content creation
----------------

The content creation allows to define a ``content_creation`` folder in any
generic setup profile folder, containing JSON-files with definitions of the
content to create.

*Content creation features*

- JSON based definition
- construct instances of any archetypes FTIs
- add file- and image-fields
- create topic criterions
- execute workflow transition on creation
- create placeful workflow policies
- set properties
- set constraint types
- set per-object provided interfaces
- reindexing the catalog



Links
-----

- Main github project repository: https://github.com/4teamwork/ftw.inflator
- Issue tracker: https://github.com/4teamwork/ftw.inflator/issues
- Package on pypi: http://pypi.python.org/pypi/ftw.inflator
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.inflator


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.inflator`` is licensed under GNU General Public License, version 2.
