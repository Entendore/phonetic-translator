"""Use Case 6: Lyric Translator"""
from translator import PhoneticTranslator

class LyricTranslator:
    def __init__(self):
        self.translator = PhoneticTranslator()
    
    def translate_line(self, line: str, target_lang: str):
        src_ipa = self.translator.text_to_ipa(line, 'en')
        src_phonemes = self.translator.ipa_to_phonemes(src_ipa)
        translation = self.translator.translate(line, 'en', target_lang)
        tgt_ipa = translation['tgt_ipa']
        tgt_phonemes = self.translator.ipa_to_phonemes(tgt_ipa)
        vowels = set('iɪeɛæaɑɔoʊuʌə')
        src_syl = sum(1 for p in src_phonemes if p in vowels)
        tgt_syl = sum(1 for p in tgt_phonemes if p in vowels)
        return {
            'original': line, 'translation': translation['target'],
            'src_syllables': src_syl, 'tgt_syllables': tgt_syl,
            'singable': abs(src_syl - tgt_syl) <= 1,
            'confidence': translation['confidence']
        }

if __name__ == "__main__":
    translator = LyricTranslator()
    lyrics = ["Hello from the other side", "To tell you I'm sorry"]
    for line in lyrics:
        result = translator.translate_line(line, 'es')
        status = "✓" if result['singable'] else "✗"
        print(f"\n{status} {result['original']}")
        print(f"  → {result['translation']}")
        print(f"  Syllables: {result['src_syllables']} → {result['tgt_syllables']}")
