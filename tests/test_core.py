"""Tests for core PhoneticTranslator."""
import pytest
from translator import PhoneticTranslator


class TestPhoneticTranslatorInit:
    def test_creates_instance(self):
        t = PhoneticTranslator()
        assert t is not None

    def test_has_mapper(self, translator):
        assert translator.mapper is not None

    def test_has_p2g(self, translator):
        assert translator.p2g is not None

    def test_supported_languages_not_empty(self, translator):
        assert len(translator.supported_languages()) > 0

    def test_english_is_supported(self, translator):
        assert 'en' in translator.supported_languages()


class TestTextToIPA:
    def test_english_hello(self, translator):
        ipa = translator.text_to_ipa("hello", "en")
        assert isinstance(ipa, str)
        assert len(ipa) > 0

    def test_empty_string(self, translator):
        assert translator.text_to_ipa("", "en") == ""

    def test_whitespace_only(self, translator):
        assert translator.text_to_ipa("   ", "en") == ""

    @pytest.mark.parametrize("text", ["hello", "world", "test", "python"])
    def test_various_english_words(self, translator, text):
        ipa = translator.text_to_ipa(text, "en")
        assert isinstance(ipa, str)
        assert len(ipa) > 0


class TestIPAToPhonemes:
    def test_simple_phonemes(self, translator):
        phonemes = translator.ipa_to_phonemes("helo")
        assert phonemes == ['h', 'e', 'l', 'o']

    def test_multichar_phonemes(self, translator):
        phonemes = translator.ipa_to_phonemes("tʃɪkən")
        assert 'tʃ' in phonemes

    def test_stress_markers_removed(self, translator):
        phonemes = translator.ipa_to_phonemes("ˈhɛloʊ")
        assert 'ˈ' not in phonemes

    def test_empty_string(self, translator):
        assert translator.ipa_to_phonemes("") == []


class TestTranslate:
    def test_basic_translation(self, translator):
        result = translator.translate("hello", "en", "es")
        assert 'source' in result
        assert 'target' in result
        assert 'src_ipa' in result
        assert 'tgt_ipa' in result
        assert 'confidence' in result

    def test_result_types(self, translator):
        result = translator.translate("hello", "en", "es")
        assert isinstance(result['source'], str)
        assert isinstance(result['target'], str)
        assert isinstance(result['confidence'], float)

    def test_confidence_range(self, translator):
        result = translator.translate("hello", "en", "es")
        assert 0.0 <= result['confidence'] <= 1.0

    def test_source_preserved(self, translator):
        result = translator.translate("hello", "en", "es")
        assert result['source'] == "hello"
        assert result['source_lang'] == "en"
        assert result['target_lang'] == "es"

    @pytest.mark.parametrize("src,tgt", [("en", "es"), ("en", "fr"), ("en", "de")])
    def test_language_pairs(self, translator, src, tgt):
        result = translator.translate("hello", src, tgt)
        assert isinstance(result['target'], str)
        assert len(result['target']) > 0


class TestBatchTranslate:
    def test_batch_basic(self, translator, sample_translations):
        results = translator.batch_translate(sample_translations)
        assert len(results) == len(sample_translations)

    def test_batch_empty(self, translator):
        assert translator.batch_translate([]) == []


class TestPhoneticDistance:
    def test_same_phoneme_zero_distance(self, translator):
        assert translator.phonetic_distance('p', 'p') == 0.0

    def test_different_phonemes_positive_distance(self, translator):
        assert translator.phonetic_distance('p', 'b') >= 0.0
