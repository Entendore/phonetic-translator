"""Tests for phoneme-to-grapheme."""
import pytest
from translator.p2g import PhonemeToGrapheme


class TestP2GInit:
    def test_creates_instance(self):
        assert PhonemeToGrapheme() is not None


class TestConvert:
    def test_basic_english(self, p2g):
        result = p2g.convert(['h', 'ɛ', 'l', 'oʊ'], 'en')
        assert isinstance(result, str)
        assert len(result) > 0

    def test_empty_phonemes(self, p2g):
        assert p2g.convert([], 'en') == ""

    def test_english_special_phonemes(self, p2g):
        result = p2g.convert(['θ', 'ɪ', 'ŋ'], 'en')
        assert 'th' in result
        assert 'ng' in result

    def test_spanish_special_phonemes(self, p2g):
        result = p2g.convert(['tʃ', 'ɲ'], 'es')
        assert 'ch' in result
        assert 'ñ' in result

    @pytest.mark.parametrize("lang", ['en', 'es', 'fr', 'de', 'ja', 'zh'])
    def test_all_languages_produce_output(self, p2g, lang):
        result = p2g.convert(['p', 'a', 't'], lang)
        assert isinstance(result, str)
        assert len(result) > 0
