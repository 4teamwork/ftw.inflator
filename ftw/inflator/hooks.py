from Products.CMFCore.utils import getToolByName
from plone.i18n.normalizer.interfaces import IURLNormalizer
from zope.component import queryUtility
from zope.i18n.locales import locales


def setup_language(portal):
    """When installing plone, the language is set when creating
    example content.
    If the content creation profile ``Products.CMFPlone:plone-content``
    is not installed, the lanuage is not set up properly.

    This setup handler allows to only setup the language but not
    create example content by putting a ``inflator-setup-language.txt``
    in a generic setup profile which is used on initialization.

    The code of this function is copied from
    ``Products.CMFPlone.setuphandlers.setupPortalContent``.
    """
    language = portal.Language()
    parts = (language.split('-') + [None, None])[:3]
    locale = locales.getLocale(*parts)
    target_language = base_language = locale.id.language

    # If we get a territory, we enable the combined language codes
    use_combined = False
    if locale.id.territory:
        use_combined = True
        target_language += '_' + locale.id.territory

    # As we have a sensible language code set now, we disable the
    # start neutral functionality
    tool = getToolByName(portal, "portal_languages")

    tool.manage_setLanguageSettings(language,
        [language],
        setUseCombinedLanguageCodes=use_combined,
        startNeutral=False)

    # Set the first day of the week, defaulting to Sunday, as the
    # locale data doesn't provide a value for English. European
    # languages / countries have an entry of Monday, though.
    calendar = getToolByName(portal, "portal_calendar", None)
    if calendar is not None:
        first = 6
        gregorian = locale.dates.calendars.get(u'gregorian', None)
        if gregorian is not None:
            first = gregorian.week.get('firstDay', None)
            # on the locale object we have: mon : 1 ... sun : 7
            # on the calendar tool we have: mon : 0 ... sun : 6
            if first is not None:
                first = first - 1

        calendar.firstweekday = first

    # Enable visible_ids for non-latin scripts

    # See if we have an url normalizer
    normalizer = queryUtility(IURLNormalizer, name=target_language)
    if normalizer is None:
        normalizer = queryUtility(IURLNormalizer, name=base_language)
