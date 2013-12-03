from Products.CMFCore.utils import getToolByName
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from copy import deepcopy
from ftw.inflator.creation.sections.base import ObjectUpdater
from plone.uuid.interfaces import IUUIDGenerator
from zope.component import getUtility
from zope.interface import classProvides
from zope.interface import implements
import pkg_resources


try:
    pkg_resources.get_distribution('plone.app.multilingual')

except pkg_resources.DistributionNotFound:
    HAS_MULTILINGUAL = False

else:
    HAS_MULTILINGUAL = True
    from plone.app.multilingual.browser.setup import SetupMultilingualSite
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
            # XXX improve exception
            raise Exception('plone.app.multilingual is not installed')

        self._validate_languages(item['_multilingual'])

        multilingual_setup = SetupMultilingualSite()
        multilingual_setup.setupSite(self.context)

        contents = deepcopy(item['_contents'])
        self._recursive_create_translation_group(contents)

        for lang_code in item['_multilingual']:
            lang_contents = deepcopy(contents)
            self._recursive_set_language(lang_contents, lang_code)

            yield {'_path': lang_code,
                   '_children': lang_contents}

    def _validate_languages(self, languages):
        portal_languages = getToolByName(self.context, 'portal_languages')

        for lang_code in languages:
            if lang_code not in portal_languages.supported_langs:
                # XXX inprove exception
                raise Exception('lang not configured %s' % lang_code)

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
