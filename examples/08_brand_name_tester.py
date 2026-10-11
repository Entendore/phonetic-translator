"""Use Case 8: Brand Name Tester"""
from translator import PhoneticTranslator

class BrandNameTester:
    def __init__(self):
        self.translator = PhoneticTranslator()
    
    def test_brand(self, brand_name: str, markets: list):
        results = []
        for market in markets:
            translation = self.translator.translate(brand_name, 'en', market)
            score = translation['confidence'] * 100
            results.append({
                'market': market, 'pronunciation': translation['tgt_ipa'],
                'confidence': translation['confidence'], 'score': score
            })
        return {'brand': brand_name, 'results': sorted(results, key=lambda x: -x['score'])}

if __name__ == "__main__":
    tester = BrandNameTester()
    result = tester.test_brand("Nova", ['es', 'fr', 'de', 'it', 'ja', 'zh'])
    print(f"BRAND TEST: {result['brand'].upper()}\n")
    for r in result['results']:
        status = "✓" if r['score'] > 70 else "⚠" if r['score'] > 50 else "✗"
        print(f"{status} {r['market'].upper()}: {r['pronunciation']} (Score: {r['score']:.0f})")
