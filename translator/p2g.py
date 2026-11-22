"""
Phoneme-to-grapheme conversion.
"""
from typing import List, Dict


class PhonemeToGrapheme:
    """Convert phonemes back to text."""
    
    P2G_TABLES = {
        'en': {
            'θ': 'th', 'ð': 'th', 'ʃ': 'sh', 'ʒ': 's', 'ŋ': 'ng',
            'tʃ': 'ch', 'dʒ': 'j', 'ɹ': 'r', 'j': 'y',
            'ɪ': 'i', 'ɛ': 'e', 'æ': 'a', 'ɑ': 'a', 'ɔ': 'o',
            'ʊ': 'oo', 'ʌ': 'u', 'ə': 'a',
        },
        'es': {
            'θ': 'z', 'ð': 'd', 'ʃ': 'ch', 'tʃ': 'ch', 'ɲ': 'ñ',
            'x': 'j', 'ɾ': 'r', 'r': 'rr',
        },
        'fr': {
            'ʃ': 'ch', 'ʒ': 'j', 'ɲ': 'gn', 'ʁ': 'r', 'ø': 'oe',
            'œ': 'oe', 'y': 'u', 'ŋ': 'ng',
        },
        'de': {
            'ʃ': 'sch', 'x': 'ch', 'ç': 'ch', 'ʁ': 'r', 'y': 'ü',
            'ø': 'ö', 'ŋ': 'ng',
        },
        'it': {
            'ʃ': 'sc', 'ʎ': 'gl', 'ɲ': 'gn', 'ʤ': 'g', 'ʧ': 'c',
        },
        'ja': {
            'ɕ': 'sh', 'ʑ': 'j', 'tɕ': 'ch', 'dʑ': 'j', 'ɸ': 'f',
            'ɲ': 'ny', 'ɯ': 'u',
        },
        'zh': {
            'ɕ': 'x', 'ʂ': 'sh', 'ʐ': 'r', 'tɕ': 'j', 'tɕʰ': 'q',
            'tʂ': 'zh', 'tʂʰ': 'ch', 'ɤ': 'e', 'ŋ': 'ng',
        },
    }
    
    def convert(self, phonemes: List[str], lang: str) -> str:
        table = self.P2G_TABLES.get(lang, {})
        result = []
        for p in phonemes:
            if p in table:
                result.append(table[p])
            else:
                result.append(p)
        return ''.join(result)
