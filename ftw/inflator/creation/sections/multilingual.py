from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from copy import deepcopy
from ftw.inflator import HAS_MULTILINGUAL
from ftw.inflator import IS_PLONE_5
from ftw.inflator import IS_PLONE_APP_MULTILINGUAL_2
from ftw.inflator.creation.sections.base import ObjectUpdater
from ftw.inflator.exceptions import MultilingalInflateException
from plone.uuid.interfaces import IUUIDGenerator
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.interface import classProvides
from zope.interface import implements


if HAS_MULTILINGUAL:
    from plone.app.multilingual.browser.setup import SetupMultilingualSite
    if IS_PLONE_5 or IS_PLONE_APP_MULTILINGUAL_2:
        if IS_PLONE_5:
            from Products.CMFPlone.interfaces import ILanguage
        else:
            from plone.app.multilingual.interfaces import ILanguage
        from plone.app.multilingual.interfaces import IMutableTG
        from plone.app.multilingual.interfaces import ITranslationManager
    else:
        # plone.app.multilingual 1.x
        from plone.multilingual.interfaces import ILanguage
        from plone.multilingual.interfaces import IMutableTG
        from plone.multilingual.interfaces import ITranslationManager


class SetupLanguages(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context

    def __iter__(self):
        for item in self.previous:
            if '_multilingual' in item:
                for subitem in self.setup_languages(item):
                    yield subitem
            else:
                yield item

    def setup_languages(self, item):
        if not HAS_MULTILINGUAL:
            raise MultilingalInflateException(
                "Defined multilingal content but plone.app.multilingual is "
                "not installed")

        self._validate_languages(item['_multilingual'])

        multilingual_setup = SetupMultilingualSite()

        if IS_PLONE_5 or IS_PLONE_APP_MULTILINGUAL_2:
            if '_folder_type_language_independent' in item:
                multilingual_setup.folder_type_language_independent = \
                    item['_folder_type_language_independent']

        if '_folder_type' in item:
            multilingual_setup.folder_type = item['_folder_type']

        if IS_PLONE_5:
            # plone.app.multilingual 5.x is setting up the languagefolders
            # automatically after installing the product.
            # There is no possiblity to hook in this process. To be able to
            # use our own types anyway, we remove the creted language-folders,
            # and run our won setup with custom configuration.
            #
            # See https://github.com/plone/plone.app.multilingual/blob/5.2.x/src/plone/app/multilingual/setuphandlers.py#L33
            catalog = getToolByName(self.context, 'portal_catalog')
            for brain in catalog(portal_type="LRF"):
                obj = brain.getObject()
                obj.aq_parent.manage_delObjects([obj.getId()])

        multilingual_setup.setupSite(self.context)

        contents = deepcopy(item['_contents'])
        self._recursive_create_translation_group(contents)

        for lang_code in item['_multilingual']:
            lang_contents = deepcopy(contents)
            self._recursive_set_language(lang_contents, lang_code)

            subitem = {'_path': lang_code,
                       '_children': lang_contents}
            if '_properties' in item:
                subitem['_properties'] = deepcopy(item['_properties'])
            yield subitem

    def _validate_languages(self, languages):
        portal_languages = getToolByName(self.context, 'portal_languages')

        if IS_PLONE_5:
            msg = ("Language '{}' is not configured. Configured languages "
                   "are: '{}'. Check if a registry.xml is available and "
                   "if it contains all required languages.")
        else:
            msg = ("Language '{}' is not configured. Configured languages "
                   "are: '{}'. Check if portal_languages.xml is available and "
                   "if it contains all required languages.")

        for lang_code in languages:
            if lang_code not in portal_languages.supported_langs:
                raise MultilingalInflateException(msg.format(
                    lang_code,
                    ','.join(portal_languages.supported_langs)))

    def _recursive_create_translation_group(self, items):
        uuid_generator = getUtility(IUUIDGenerator)

        for item in items:
            item['_multilingual_settings'] = {
                'translation_group_uuid': uuid_generator()}

            if '_children' in item:
                self._recursive_create_translation_group(item['_children'])

    def _recursive_set_language(self, items, lang_code):
        for item in items:
            item['_multilingual_settings']['language'] = lang_code
            if '_children' in item:
                self._recursive_set_language(item['_children'], lang_code)


class LinkMultilingualContent(ObjectUpdater):
    classProvides(ISectionBlueprint)

    key_option_name = 'multilingual-settings-key'
    default_key_name = 'multilingual_settings'

    def update(self, obj, data):
        ILanguage(obj).set_language(data['language'])
        IMutableTG(obj).set(data['translation_group_uuid'])

        manager = ITranslationManager(obj)
        manager.register_translation(data['language'], obj)
