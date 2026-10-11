"""
Core phonetic translator using real libraries.
"""
from typing import List, Dict, Optional, Tuple
import logging

try:
    import epitran
    EPITRAN_AVAILABLE = True
except ImportError:
    EPITRAN_AVAILABLE = False

try:
    import g2p_en
    G2P_EN_AVAILABLE = True
except ImportError:
    G2P_EN_AVAILABLE = False

try:
    import panphon
    PANPHON_AVAILABLE = True
except ImportError:
    PANPHON_AVAILABLE = False

from .mapping import PhonemeMapper
from .p2g import PhonemeToGrapheme

logger = logging.getLogger(__name__)


class PhoneticTranslator:
    """
    Practical phonetic translator: text → IPA → target text.
    
    Uses real libraries:
    - epitran: G2P for 70+ languages
    - g2p_en: English G2P (neural)
    - panphon: phonetic distance
    
    Example:
        >>> t = PhoneticTranslator()
        >>> t.translate("hello", "en", "es")
        {'source': 'hello', 'target': 'helo', 'src_ipa': 'hɛloʊ', 'tgt_ipa': 'helo'}
    """
    
    LANGUAGE_CODES = {
        'en': 'eng-Latn', 'es': 'spa-Latn', 'fr': 'fra-Latn',
        'de': 'deu-Latn', 'it': 'ita-Latn', 'pt': 'por-Latn',
        'nl': 'nld-Latn', 'ru': 'rus-Cyrl', 'zh': 'cmn-Hans',
        'ja': 'jpn-Jpan', 'ko': 'kor-Kore', 'ar': 'ara-Arab',
        'hi': 'hin-Deva', 'tr': 'tur-Latn', 'pl': 'pol-Latn',
        'sv': 'swe-Latn', 'vi': 'vie-Latn', 'th': 'tha-Thai',
    }
    
    def __init__(self):
        self._init_g2p()
        self._init_distance()
        self.mapper = PhonemeMapper()
        self.p2g = PhonemeToGrapheme()
    
    def _init_g2p(self):
        self.epitran_engines = {}
        self.g2p_en = None
        
        if EPITRAN_AVAILABLE:
            for lang_code, epitran_code in self.LANGUAGE_CODES.items():
                try:
                    self.epitran_engines[lang_code] = epitran.Epitran(epitran_code)
                    logger.info(f"Loaded epitran for {lang_code}")
                except Exception as e:
                    logger.warning(f"Failed to load epitran for {lang_code}: {e}")
        
        if G2P_EN_AVAILABLE:
            try:
                self.g2p_en = g2p_en.G2p()
                logger.info("Loaded g2p_en")
            except Exception as e:
                logger.warning(f"Failed to load g2p_en: {e}")
    
    def _init_distance(self):
        self.ft = None
        if PANPHON_AVAILABLE:
            try:
                self.ft = panphon.FeatureTable()
                logger.info("Loaded panphon")
            except Exception as e:
                logger.warning(f"Failed to load panphon: {e}")
    
    def text_to_ipa(self, text: str, lang: str) -> str:
        text = text.strip()
        if not text:
            return ""
        
        if lang == 'en' and self.g2p_en:
            try:
                arpabet = self.g2p_en(text)
                return self._arpabet_to_ipa(arpabet)
            except Exception as e:
                logger.warning(f"g2p_en failed: {e}")
        
        if lang in self.epitran_engines:
            try:
                return self.epitran_engines[lang].transliterate(text)
            except Exception as e:
                logger.warning(f"epitran failed: {e}")
        
        return self._fallback_g2p(text, lang)
    
    def _arpabet_to_ipa(self, arpabet) -> str:
        ARPABET_TO_IPA = {
            'AA': 'ɑ', 'AE': 'æ', 'AH': 'ʌ', 'AO': 'ɔ', 'AW': 'aʊ',
            'AY': 'aɪ', 'B': 'b', 'CH': 'tʃ', 'D': 'd', 'DH': 'ð',
            'EH': 'ɛ', 'ER': 'ɝ', 'EY': 'eɪ', 'F': 'f', 'G': 'ɡ',
            'HH': 'h', 'IH': 'ɪ', 'IY': 'i', 'JH': 'dʒ', 'K': 'k',
            'L': 'l', 'M': 'm', 'N': 'n', 'NG': 'ŋ', 'OW': 'oʊ',
            'OY': 'ɔɪ', 'P': 'p', 'R': 'ɹ', 'S': 's', 'SH': 'ʃ',
            'T': 't', 'TH': 'θ', 'UH': 'ʊ', 'UW': 'u', 'V': 'v',
            'W': 'w', 'Y': 'j', 'Z': 'z', 'ZH': 'ʒ',
        }
        result = []
        for token in arpabet:
            token = token.strip()
            if not token:
                continue
            clean = ''.join(c for c in token if not c.isdigit())
            if clean in ARPABET_TO_IPA:
                result.append(ARPABET_TO_IPA[clean])
            elif clean:
                result.append(clean)
        return ''.join(result)
    
    def _fallback_g2p(self, text: str, lang: str) -> str:
        return text.lower()
    
    def ipa_to_phonemes(self, ipa: str) -> List[str]:
        multi_char = ['tʃ', 'dʒ', 'ts', 'dz', 'aɪ', 'aʊ', 'eɪ', 'oʊ', 'ɔɪ']
        phonemes = []
        i = 0
        while i < len(ipa):
            matched = False
            for mc in multi_char:
                if ipa.startswith(mc, i):
                    phonemes.append(mc)
                    i += len(mc)
                    matched = True
                    break
            if not matched:
                if ipa[i] not in 'ˈˌː.':
                    phonemes.append(ipa[i])
                i += 1
        return phonemes
    
    def phonetic_distance(self, p1: str, p2: str) -> float:
        if self.ft:
            try:
                return self.ft.weighted_hamming_distance(p1, p2)
            except Exception:
                pass
        return 0.0 if p1 == p2 else 1.0
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> Dict:
        src_ipa = self.text_to_ipa(text, source_lang)
        src_phonemes = self.ipa_to_phonemes(src_ipa)
        tgt_phonemes = self.mapper.map_sequence(src_phonemes, target_lang)
        tgt_ipa = ''.join(tgt_phonemes)
        tgt_text = self.p2g.convert(tgt_phonemes, target_lang)
        confidence = self._compute_confidence(src_phonemes, tgt_phonemes)
        
        return {
            'source': text,
            'target': tgt_text,
            'src_ipa': src_ipa,
            'tgt_ipa': tgt_ipa,
            'src_phonemes': src_phonemes,
            'tgt_phonemes': tgt_phonemes,
            'confidence': confidence,
            'source_lang': source_lang,
            'target_lang': target_lang,
        }
    
    def _compute_confidence(self, src: List[str], tgt: List[str]) -> float:
        if not src or not tgt:
            return 0.0
        total_dist = 0.0
        count = 0
        for s, t in zip(src, tgt):
            dist = self.phonetic_distance(s, t)
            total_dist += dist
            count += 1
        if count == 0:
            return 0.0
        avg_dist = total_dist / count
        return round(max(0.0, 1.0 - (avg_dist / 10.0)), 3)
    
    def batch_translate(self, items: List[Tuple[str, str, str]]) -> List[Dict]:
        results = []
        for text, src, tgt in items:
            try:
                result = self.translate(text, src, tgt)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to translate '{text}': {e}")
                results.append({'source': text, 'target': '', 'error': str(e)})
        return results
    
    def supported_languages(self) -> List[str]:
        return sorted(self.LANGUAGE_CODES.keys())
