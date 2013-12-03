#!/usr/bin/env sh

if [[ "$0" != "./update-translations.sh" ]]; then
    echo "Run from ftw/inflator/tests with ./update-translations.sh"
    exit 1
fi


cat > ftw.inflator.tests.pot <<EOF
# --- PLEASE EDIT THE LINES BELOW CORRECTLY ---
# SOME DESCRIPTIVE TITLE.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\n"
"POT-Creation-Date: 2013-02-01 16:26+0000\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI +ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=utf-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=1; plural=0\n"
"Language-Code: en\n"
"Language-Name: English\n"
"Preferred-Encodings: utf-8 latin1\n"
"Domain: ftw.inflator.tests\n"
EOF

for msgid in $(grep -r ":translate(ftw.inflator.tests)" ../profiles | sed -e 's/.*: "\([^"]*\)",*$/\1/g'); do
    echo "" >> ftw.inflator.tests.pot
    echo "msgid \"$msgid\"" >> ftw.inflator.tests.pot
    echo "msgstr \"\"" >> ftw.inflator.tests.pot
done

i18ndude sync --pot ftw.inflator.tests.pot en/LC_MESSAGES/ftw.inflator.tests.po
i18ndude sync --pot ftw.inflator.tests.pot de/LC_MESSAGES/ftw.inflator.tests.po
