from googletrans import Translator

def word_translate(text: str, dest_lang: str) -> str:
    translator = Translator()
    return translator.translate(text=text, dest=dest_lang).text
    
     