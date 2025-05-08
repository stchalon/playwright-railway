from googletrans import Translator

def translate_text_to_french(text, max_chars=3000):
    translator = Translator()
    chunks = [text[i:i + max_chars] for i in range(0, len(text), max_chars)]
    translated = [translator.translate(chunk, dest="fr").text for chunk in chunks]
    return "\n\n".join(translated)
