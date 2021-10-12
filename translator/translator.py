from googletrans import Translator

def word_translate(text: str, dest_lang: str) -> str:
    translator = Translator()
    translated_text = translator.translate(text=text, dest=dest_lang).text
    if text.islower():
        translated_text.lower()
    return translated_text
    
     