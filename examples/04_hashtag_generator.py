"""Use Case 4: Hashtag Generator"""
from translator import PhoneticTranslator

class HashtagGenerator:
    def __init__(self):
        self.translator = PhoneticTranslator()
    
    def generate_hashtags(self, phrase: str, languages: list):
        hashtags = [{'lang': 'en', 'hashtag': '#' + ''.join(c for c in phrase if c.isalnum()).lower()}]
        for lang in languages:
            translation = self.translator.translate(phrase, 'en', lang)
            hashtag = '#' + ''.join(c for c in translation['tgt_ipa'] if c.isalnum()).lower()
            hashtags.append({'lang': lang, 'hashtag': hashtag})
        return {'original': phrase, 'hashtags': hashtags}

if __name__ == "__main__":
    generator = HashtagGenerator()
    result = generator.generate_hashtags("Good Vibes", ['es', 'fr', 'de', 'ja'])
    print(f"Original: {result['original']}\n")
    for h in result['hashtags']:
        print(f"  {h['lang'].upper()}: {h['hashtag']}")
