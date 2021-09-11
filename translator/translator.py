from googletrans import Translator

def word_translate(text: str, dest: str) -> str:
    translator = Translator()
    return translator.translate(text=text, dest=dest).text
    
     