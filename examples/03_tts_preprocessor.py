"""Use Case 3: TTS Preprocessor"""
from translator import PhoneticTranslator

class TTSPreprocessor:
    def __init__(self):
        self.translator = PhoneticTranslator()
    
    def prepare_for_tts(self, text: str, lang: str = 'en'):
        ipa = self.translator.text_to_ipa(text, lang)
        words = text.split()
        phonetic_words = []
        for word in words:
            word_ipa = self.translator.text_to_ipa(word, lang)
            phonetic_words.append({
                'text': word, 'ipa': word_ipa,
                'phonemes': self.translator.ipa_to_phonemes(word_ipa)
            })
        return {'original': text, 'full_ipa': ipa, 'words': phonetic_words}

if __name__ == "__main__":
    preprocessor = TTSPreprocessor()
    result = preprocessor.prepare_for_tts("The quick brown fox")
    print(f"Original: {result['original']}")
    print(f"Full IPA: {result['full_ipa']}\n")
    for w in result['words']:
        print(f"  {w['text']}: {w['ipa']}")
