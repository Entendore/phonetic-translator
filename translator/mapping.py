"""
Phoneme mapping between languages using panphon.
"""
from typing import List, Dict
import logging

try:
    import panphon
    PANPHON_AVAILABLE = True
except ImportError:
    PANPHON_AVAILABLE = False

logger = logging.getLogger(__name__)


class PhonemeMapper:
    """Maps phonemes between languages using phonetic distance."""
    
    INVENTORIES = {
        'en': list('pbtdkɡfvθðszʃʒhmnlɹwtʃdʒiɪeɛæɑɔoʊuʌə'),
        'es': list('pbtdkɡfθsxʧmnlɾjwiɛaou'),
        'fr': list('pbtdkɡfvsʒʁmnlɲŋjwiɛaɔouyəøœ'),
        'de': list('pbtdkɡʔfvsxçhmnlɹŋjwiɪeɛaɑɔoʊuyøə'),
        'it': list('pbtdkɡfvstsdzʃʎɲmnlɹjwiɛaɔou'),
        'pt': list('pbtdkɡfvstʃʒɲmnlɹʁjwiɛaɔou'),
        'ja': list('kɡstdʑnɲhɸbmprɹjwɯaeio'),
        'zh': list('pbtdkɡfsʂʃxɕhtɕtɕʰtʂtʂʰmnljwiyeuɤəaoe'),
        'ko': list('pʰptʰtkʰkɡnɲmɸsʰszʑhɹlɾiɛaʌu'),
        'ru': list('pbtdkɡfvθðszʃʒhmnlrwtʃdʒiɪeɛæɑɔouʌə'),
    }
    
    def __init__(self):
        self.ft = None
        if PANPHON_AVAILABLE:
            try:
                self.ft = panphon.FeatureTable()
            except Exception as e:
                logger.warning(f"Failed to load panphon: {e}")
    
    def get_inventory(self, lang: str) -> List[str]:
        return self.INVENTORIES.get(lang, list('pbtdkɡfvθðszʃʒhmnlɹwiɛaou'))
    
    def find_closest(self, phoneme: str, target_lang: str) -> str:
        inventory = self.get_inventory(target_lang)
        if phoneme in inventory:
            return phoneme
        if not self.ft:
            return self._simple_mapping(phoneme, target_lang)
        best = phoneme
        best_dist = float('inf')
        for candidate in inventory:
            try:
                dist = self.ft.weighted_hamming_distance(phoneme, candidate)
                if dist < best_dist:
                    best_dist = dist
                    best = candidate
            except Exception:
                continue
        return best
    
    def _simple_mapping(self, phoneme: str, target_lang: str) -> str:
        MAPPINGS = {
            'θ': {'es': 'd', 'fr': 's', 'de': 'z', 'ja': 's'},
            'ð': {'es': 'd', 'fr': 'z', 'de': 'd', 'ja': 'z'},
            'ʃ': {'es': 'tʃ', 'ja': 'ɕ'},
            'ʒ': {'es': 'ʧ', 'ja': 'ʑ'},
            'ŋ': {'es': 'n', 'fr': 'n', 'ja': 'n'},
            'æ': {'es': 'e', 'fr': 'a', 'de': 'ɛ', 'ja': 'a'},
            'ʌ': {'es': 'a', 'fr': 'a', 'de': 'a', 'ja': 'a'},
            'ɹ': {'ja': 'ɾ', 'es': 'r', 'fr': 'ʁ'},
        }
        if phoneme in MAPPINGS and target_lang in MAPPINGS[phoneme]:
            return MAPPINGS[phoneme][target_lang]
        return phoneme
    
    def map_sequence(self, phonemes: List[str], target_lang: str) -> List[str]:
        return [self.find_closest(p, target_lang) for p in phonemes]
