"""Use Case 7: Travel Phrase Guide"""
from translator import PhoneticTranslator

class TravelPhraseGuide:
    def __init__(self):
        self.translator = PhoneticTranslator()
        self.phrases = ['Hello', 'Thank you', 'Please', 'Goodbye', 'Sorry', 'Where is']
    
    def generate_guide(self, target_lang: str):
        guide = []
        for phrase in self.phrases:
            translation = self.translator.translate(phrase, 'en', target_lang)
            guide.append({
                'english': phrase, 'translation': translation['target'],
                'pronunciation': translation['tgt_ipa'],
                'confidence': translation['confidence']
            })
        return guide

if __name__ == "__main__":
    guide = TravelPhraseGuide().generate_guide('es')
    print("SPANISH TRAVEL PHRASES\n")
    for p in guide:
        print(f"{p['english']}")
        print(f"  {p['translation']}  /{p['pronunciation']}/")
        print(f"  Confidence: {p['confidence']:.0%}\n")
