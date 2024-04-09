import os
import json

class MultiLanguage:
    def __init__(self, folder: str):
        self.translations = {}
        self.load_translations(folder)

    def load_translations(self, folder: str):
        for filename in os.listdir(folder):
            if filename.endswith('.json'):
                language_code = filename[:-5]  # Extract language code from filename
                file_path = os.path.join(folder, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    translations = json.load(file)
                    self.translations[language_code] = translations

    def get(self, text_name: str, language: str, **kwargs) -> str:
        language_translations: dict = self.translations.get(language, {})
        formatted_text:str = language_translations.get(text_name, text_name)  # Return text_name if translation not found
        return formatted_text.format(**kwargs)


    def get_all(self, *text_names, **kwargs):
        all_texts = []

        for language_code, translations in self.translations.items():
            for text_name in text_names:
                translated_text = translations.get(text_name, text_name)
                formatted_text = translated_text.format(**kwargs)
                all_texts.append( formatted_text)

        return all_texts

multilanguage = MultiLanguage("locales")
