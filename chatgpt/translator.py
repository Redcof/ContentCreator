from translate import Translator
from googletrans import Translator as googleTranslator


def text_translate(src_text, src_lang, dest_lang):
    translate = Translator(from_lang=src_lang, to_lang=dest_lang)
    translation = translate.translate(src_text)
    return translation


def google_translate_text(text, target_language):
    translator = googleTranslator(service_urls=['translate.google.com'])
    translation = translator.translate(text, dest=target_language)
    return translation.text
