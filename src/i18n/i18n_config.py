import os
from gettext import translation, NullTranslations

class I18n:
    def __init__(self, locale_dir="locales", default_language="en"):
        self.locale_dir = locale_dir
        self.default_language = default_language
        self.translations = {}

    def load_translations(self, languages):
        for lang in languages:
            try:
                self.translations[lang] = translation(
                    "messages", localedir=self.locale_dir, languages=[lang]
                )
            except FileNotFoundError:
                self.translations[lang] = NullTranslations()

    def gettext(self, lang, message):
        if lang in self.translations:
            return self.translations[lang].gettext(message)
        return message  # Fallback to the original message

# Initialize i18n
i18n = I18n()
i18n.load_translations(["en", "es", "fr", "de", "zh"])
