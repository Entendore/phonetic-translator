"""Use Case 2: Product Name Validator"""
from translator import PhoneticTranslator

class ProductNameValidator:
    def __init__(self):
        self.translator = PhoneticTranslator()
    
    def validate_name(self, product_name: str, target_markets: list):
        results = []
        for market in target_markets:
            translation = self.translator.translate(product_name, 'en', market)
            confidence = translation['confidence']
            results.append({
                'market': market,
                'pronunciation': translation['tgt_ipa'],
                'confidence': confidence,
                'recommendation': "✓ Good" if confidence > 0.8 else "⚠ Okay" if confidence > 0.6 else "✗ Poor"
            })
        return {'product_name': product_name, 'markets': results}

if __name__ == "__main__":
    validator = ProductNameValidator()
    result = validator.validate_name("Zyphr", ['es', 'fr', 'de', 'ja', 'zh'])
    print(f"Product: {result['product_name']}\n")
    for market in result['markets']:
        print(f"{market['market'].upper()}: {market['pronunciation']} ({market['confidence']:.0%}) - {market['recommendation']}")
