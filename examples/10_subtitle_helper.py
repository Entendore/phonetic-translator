"""Use Case 10: Subtitle Pronunciation Helper"""
from translator import PhoneticTranslator

class SubtitleHelper:
    def __init__(self):
        self.translator = PhoneticTranslator()
        self.foreign_words = ['Schwarzenegger', 'Dostoevsky', 'Nguyen', 'Miyazaki',
                              'Versailles', 'Reykjavik', 'croissant', 'bruschetta']
    
    def generate_hints(self, subtitle_text: str):
        hints = []
        for word in self.foreign_words:
            if word.lower() in subtitle_text.lower():
                ipa = self.translator.text_to_ipa(word, 'en')
                hints.append({'word': word, 'ipa': ipa})
        return {'subtitle': subtitle_text, 'hints': hints}

if __name__ == "__main__":
    helper = SubtitleHelper()
    result = helper.generate_hints("Arnold Schwarzenegger had a croissant.")
    print(f"Subtitle: {result['subtitle']}\n")
    print("Pronunciation hints:")
    for hint in result['hints']:
        print(f"  {hint['word']}: /{hint['ipa']}/")
