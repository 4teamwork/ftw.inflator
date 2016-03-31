ftw.inflator
============


This packages helps predefining a Plone site setup including content
creation (using generic setup), defining multiple bundles and a wizard
for installing a new site with a bundle.


.. contents:: Table of Contents


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

.. code:: ini

    [instance]
    eggs +=
        ftw.inflator


Dexterity support
~~~~~~~~~~~~~~~~~

For beeing able to create dexterity objects (Content Creation), install the `dexterity` extras:

.. code:: ini

    [instance]
    eggs +=
        ftw.inflator [dexterity]


Compatibility
-------------


Plone 4.2

.. image:: https://jenkins.4teamwork.ch/job/ftw.inflator-master-test-plone-4.2.x.cfg/badge/icon
   :target: https://jenkins.4teamwork.ch/job/ftw.inflator-master-test-plone-4.2.x.cfg

Plone 4.3

.. image:: https://jenkins.4teamwork.ch/job/ftw.inflator-master-test-plone-4.3.x.cfg/badge/icon
   :target: https://jenkins.4teamwork.ch/job/ftw.inflator-master-test-plone-4.3.x.cfg


Setup wizard
------------

On the `manage_main` view of the Zope app there is an additional button
for installing your product.
It leads to the site setup wizard where an ID and a bundle can be selected.

The setup wizard allows to select one of a set of predefined bundles.
See the bundle section for details on how to define bundles.

.. image:: https://raw.github.com/4teamwork/ftw.inflator/master/docs/inflate.png


Wizard customizations
~~~~~~~~~~~~~~~~~~~~~

The product name and logo can easily be customized through ZCML:

.. code:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:inflator="http://namespaces.zope.org/inflator"
        i18n_domain="my.package">

        <include package="ftw.inflator" file="meta.zcml" />

        <inflator:customize
            product="Product Name"
            image="resources/product-logo.png"
            />

    </configure>


Bundle system
-------------

A bundle defines a list of profiles which are automatically applied when
creating a new Plone site with this bundle.

It has a base-profile (defaults to the Plone default base profile without
default content).

Defining bundles
~~~~~~~~~~~~~~~~

The bundles are defined in ZCML:

.. code:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:inflator="http://namespaces.zope.org/inflator"
        i18n_domain="my.package">

        <include package="ftw.inflator" file="meta.zcml" />

        <inflator:bundle
            title="ftw.inflator example bundle one"
            profiles="plonetheme.sunburst:default
                      my.policy:default
                      my.policy:init-content"
            />

    </configure>

ZCML-Attributes
~~~~~~~~~~~~~~~

title
    The (translatable) title of the bundle, shown in the setup wizard.

profiles
    One or multiple Generic Setup profiles (without ``profile-``-prefix).

description (optional)
    The description of the bundle, shown in the setup wizard.

base (optional)
    The Generic Setup base profile for creating the plone site.
    This defaults to ``Products.CMFPlone:plone``, the default plone base
    profile without content creation.
    Using ``Products.CMFPlone:plone-content`` will generate the default
    example content.

standard (optional)
    By using the standard flag (``standard="True"``) you can define product bundles.
    When registering custom bundles later without flagging them as standard, they
    will appear above the standard bundles in the setup wizard and top is selected.


Full ZCML example:

.. code:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:inflator="http://namespaces.zope.org/inflator"
        i18n_domain="ftw.inflator">

        <include package="ftw.inflator" file="meta.zcml" />

        <inflator:bundle
            title="MyProduct with sunburst"
            description="Installs MyProduct with the sunburst theme and plone default content"
            profiles="plonetheme.sunburst:default
                      my.product:default"
            base="Products.CMFPlone:plone-content"
            standard="True"
            />

    </configure>


Setting the language
~~~~~~~~~~~~~~~~~~~~

When installing a Plone site with the default add-site view, the language
is set in the ``Products.CMFPlone:plone-content``, which also creates example content.
This makes it hard to setup the language without creating the example content.

To solve this issue ``ftw.inflator`` provides a ``ftw.inflator:setup-language`` generic
setup profile, meant to be used while setting up a bundle.
You can add it to the list of bundle profiles. This sets the language of the Plone site
to the one selected in the setup wizard.
Using it as a dependency (in ``metadata.xml``) is not recommended, since it is not meant
to be used on a existing plone site.

Example usage in bundle definition:

.. code:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:inflator="http://namespaces.zope.org/inflator"
        i18n_domain="my.package">

        <include package="ftw.inflator" file="meta.zcml" />

        <inflator:bundle
            title="ftw.inflator example bundle one"
            profiles="ftw.inflator:setup-language
                      my.policy:default"
            />

    </configure>


Content creation
----------------

The content creation allows to define a ``content_creation`` folder in any
generic setup profile folder, containing JSON-files with definitions of the
content to create. The content is created when the generic setup profile is
applied.

Content creation features
~~~~~~~~~~~~~~~~~~~~~~~~~

- JSON based definition
- support for tree structure
- internationalization of strings
- construct instances of any archetypes FTIs
- add file- and image-fields
- create topic criterions
- execute workflow transition on creation
- create placeful workflow policies
- set properties
- set constraint types
- set per-object provided interfaces
- reindexing the catalog
- define and block local roles

Structure
~~~~~~~~~

Add a ``content_creation`` folder to your generic setup profile. All content
creation configurations are within this folder.
You can add as many ``*.json``-files as you want - they will be read
and executed in order of the sorted filename
(use integer prefixes for sorting them easily).

Folder creation example
~~~~~~~~~~~~~~~~~~~~~~~

For creating content create a JSON file (
e.g. ``profiles/default/content_creation/01-foo-folder.json``) and insert a
JSON syntax list of hashes (dicts).
Each hash creates a new object.
Example creating a folder with title "Foo" at ``/Plone/foo``:

.. code:: javascript

    [
        {
            "_path": "foo",
            "_type": "Folder",
            "title": "Foo"
        }
    ]


Tree structure example
~~~~~~~~~~~~~~~~~~~~~~

For nested structures it sometimes useful to define the JSON as tree.
Using the tree structure it is not necessary to repeat the path of the parent:

.. code:: javascript

    [
        {
            "_path": "foo",
            "_type": "Folder",
            "title": "Foo",
            "_children": [

                {
                    "_id": "bar",
                    "_type": "Folder",
                    "title": "Bar"
                },
                {
                    "_path": "bar/qux",
                    "_type": "Folder",
                    "title": "Bar"
                }

            ]
        }
    ]

Be sure that the root node has a `_path` and all nodes in a `_children` list
have either an `_id` or a `_path`. The `_path` of a child node is considered to be relative to the parent node. The paths will then be automatically concatenated.


Internationalization
~~~~~~~~~~~~~~~~~~~~

Using the `key:translate(domain)` syntax in keys, the respective string value is
translated to the current default language of the Plone site.
When creating content while installing a bundle with inflator, be sure to install
the generic setup profile ``ftw.inflator:setup-language`` before creating the
content.
This will make sure the language is properly configured.

Example:

.. code:: javascript

    [
        {
            "_path": "foo",
            "_type": "Folder",
            "title:translate(my.domain)": "Foo",
            "_children": [

                {
                    "_id:translate(my.domain)": "bar",
                    "_type": "Folder",
                    "title": "Bar"
                }

            ]
        }
    ]


Multilingual support
~~~~~~~~~~~~~~~~~~~~

When `plone.app.multilingual <https://pypi.python.org/pypi/plone.app.multilingual>`_ is installed
translated content can be generated for each language.
The translation is based on the `key:translate(domain)` syntax (see above) and can be translated
in regular .po-files.

Example:

.. code:: javascript

    [
        {"_multilingual": [
            "en",
            "de"],

         "_contents": [

             {
               "_id": "foo",
               "_type": "Folder",
               "title:translate(my.domain)": "Foo"
             }

         ]}
    ]

Make sure that each language in the "_multilingual" list is configured as supported
language in the `portal_languages.xml`:

.. code:: xml

    <?xml version="1.0"?>
    <object>
        <default_language value="en"/>
        <supported_langs>
            <element value="en"/>
            <element value="de"/>
        </supported_langs>
    </object>

The default setup of `plone.app.multilingual` is used for setting up the language folders.



Creating / setting properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Properties can easily be created.
If there already is a property (because the object exists already), it is
updated.

Example:

.. code:: javascript

    [
        {
            "_path": "foo",
            "_type": "Folder",
            "title": "Foo",
            "_properties": {
                "layout": ["string", "folder_listing_view"]
            }
        }
    ]


Configuring constrain types
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For configuring the addable types on a folder, use the ``_constrain_types``
keyword:

.. code:: javascript

    [
        {
            "_path": "foo",
            "_type": "Folder",
            "title": "Foo",
            "_constrain_types": {
                "locally": ["Folder", "Document"],
                "immediately": ["Folder"]
            }
        }
    ]



Provide additional interfaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By passing a list of dottednames as ``_interfaces`` those interfaces will
automatically be provided (``alsoProvides``) by the created object:

.. code:: javascript

    [
        {
            "_path": "foo",
            "_type": "Folder",
            "title": "Foo",
            "_interfaces": [
                "ftw.inflator.tests.interfaces.IFoo",
                "remove:foo.bar.interfaces.IBar"
            ]
        }
    ]

By prefixing the dotted name with ``remove:``, directly provided interfaces
can be removed (``noLongerProvides``).


Files and images
~~~~~~~~~~~~~~~~

File- and image-fields can easily be filled by using the ``:file`` postfix,
providing a relative path to the file to "upload":

.. code:: javascript

    [
        {
            "_path": "files/example-file",
            "_type": "File",
            "title": "example file",
            "file:file": "files/examplefile.txt"
        }
    ]

The filename can be changed (although this does not work with multiple files
on the same Dexterity item):

.. code:: javascript

    [
        {
            "_path": "files/example-file",
            "_type": "File",
            "title": "example file",
            "file:file": "files/lkdfahjkewrhiu.txt",
            "file:filename": "important.txt"
        }
    ]


Workflow transitions
~~~~~~~~~~~~~~~~~~~~

With the ``_transitions`` keyword it is possible to execute a workflow
transition upon content creation:

.. code:: javascript

    [
        {
            "_path": "foo",
            "_type": "Folder",
            "title": "Foo",
            "_transitions": "publish"
        }
    ]

Placeful workflow policies
~~~~~~~~~~~~~~~~~~~~~~~~~~

When placeful workflow policies are installed it is possible to activate them
on a folder using the ``_placefulworkflow`` keyword:

.. code:: javascript

      [
          {
              "_path": "intranet",
              "_type": "Folder",
              "title": "Intranet",
              "_placefulworkflow": ["intranet", "intranet"]
          }
      ]

You need to install the Generic Setup profile
``Products.CMFPlacefulWorkflow:CMFPlacefulWorkflow`` for using placeful workflow policies.


Annotations
~~~~~~~~~~~

With the ``_annotations`` it is possible to set simple annotations on the
object.
Values of type ``dict`` are converted to ``PersistentMapping``, those of
type ``list`` are converted to ``PersistentList`` recursively.
Example:

.. code:: javascript

      [
          {
              "_path": "intranet",
              "_type": "Folder",
              "title": "Intranet",
              "_annotations": {"foo": {"bar": [1, 2, 3]}}
          }
      ]


UUID Lookup
~~~~~~~~~~~

Sometimes you need to have the UUID of another object.
Since the UUID is generated randomly when creating the object you cannot
predict it in a .json-file.
The UUID lookup helps you here:

.. code:: javascript


      [
          {
              "_path": "foo",
              "_type": "MyType",
              "title": "Foo",
              "relations": "resolveUUID::bar"
          }
      ]

Using the ``resolveUUID::path`` syntax the value is replaced with UUID of the
object which has the ``path``.
You can prefix the value with a `/` for making it relative to the site root,
otherwise it is relative to the item it is defined in ("Foo" in the above
example).


Path Lookup
~~~~~~~~~~~

Sometimes you need to resolve an already created object by its path.
The resolve-path section helps you here:

.. code:: javascript


      [
          {
              "_path": "foo",
              "_type": "MyType",
              "title": "Foo",
              "relations": "resolvePath::bar"
          }
      ]

Using the ``resolvePath::path`` syntax the value is replaced with the resolved object.
You can prefix the value with a `/` for making it relative to the site root,
otherwise it is relative to the item it is defined in ("Foo" in the above
example).


Local roles example
~~~~~~~~~~~~~~~~~~~

You can configure local roles and block local as following:

.. code:: javascript


      [
          {
              "_path": "foo",
              "_type": "MyType",
              "title": "Foo",
              "_ac_local_roles": {
                  "admin": [
                      "Owner"
                  ]
              },
              "_block-local-roles": true
          }
      ]

For details, see: https://github.com/collective/collective.blueprint.jsonmigrator


Import single items
~~~~~~~~~~~~~~~~~~~

The inflator's transmogrifier config can be used in code for importing
single items by using the ``single_item_content_creation`` configuration:

.. code:: python

    item = {'_path': 'foo',
            '_type': 'Folder',
            'title': 'Foo'}

    mogrifier = Transmogrifier(portal)
    mogrifier(u'ftw.inflator.creation.single_item_content_creation',
              jsonsource=dict(item=item))


Links
-----

- Github: https://github.com/4teamwork/ftw.inflator
- Issues: https://github.com/4teamwork/ftw.inflator/issues
- Pypi: http://pypi.python.org/pypi/ftw.inflator
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.inflator


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.inflator`` is licensed under GNU General Public License, version 2.
