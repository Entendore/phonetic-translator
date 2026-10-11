"""Use Case 5: NPC Name Generator"""
from translator import PhoneticTranslator
import random

class NPCNameGenerator:
    def __init__(self):
        self.translator = PhoneticTranslator()
        self.prefixes = ['Aer', 'Thal', 'Zeph', 'Kael', 'Lyr', 'Mor', 'Syl']
        self.suffixes = ['ion', 'ius', 'ara', 'wen', 'dor', 'nis', 'thas']
    
    def generate_name(self):
        return random.choice(self.prefixes) + random.choice(self.suffixes)
    
    def validate_for_markets(self, name: str, markets: list):
        results = []
        for market in markets:
            translation = self.translator.translate(name, 'en', market)
            results.append({
                'market': market,
                'pronunciation': translation['tgt_ipa'],
                'confidence': translation['confidence'],
                'pass': translation['confidence'] > 0.7
            })
        return {'name': name, 'markets': results, 'globally_ok': all(r['pass'] for r in results)}

if __name__ == "__main__":
    generator = NPCNameGenerator()
    markets = ['es', 'fr', 'de', 'ja', 'zh']
    for _ in range(3):
        name = generator.generate_name()
        validation = generator.validate_for_markets(name, markets)
        status = "✓" if validation['globally_ok'] else "✗"
        print(f"\n{status} {name}")
        for m in validation['markets']:
            mark = "✓" if m['pass'] else "✗"
            print(f"  {mark} {m['market'].upper()}: {m['pronunciation']} ({m['confidence']:.0%})")
