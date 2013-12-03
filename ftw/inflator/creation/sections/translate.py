from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from zope.i18n import translate
from zope.interface import classProvides
from zope.interface import implements
import re


TRANSLATABLE_KEY_EXPR = re.compile(
    r'^([^:]*):translate\(([^)]*)\)$')


class Translate(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.target_language = transmogrifier.context.Language()
        self.previous = previous

    def __iter__(self):
        for item in self.previous:
            item = self.translate_recursive(item, self.target_language)
            yield item

    def translate_recursive(self, data, language):
        if isinstance(data, list):
            new_data = []
            for item in data:
                new_data.append(self.translate_recursive(item, language))

            return data

        if not isinstance(data, dict):
            return data

        if '_multilingual_settings' in data:
            language = data['_multilingual_settings']['language']

        for key, value in data.items():
            if isinstance(value, str):
                value = value.decode('utf-8')
            value = self.translate_recursive(value, language)

            match = TRANSLATABLE_KEY_EXPR.match(key)
            if not match:
                data[key] = value
                continue

            new_key, domain = match.groups()
            data[new_key] = translate(value, domain=domain,
                                      target_language=language)
            del data[key]

        return data
