"""Tests for edge cases and error handling."""
import pytest
from translator import PhoneticTranslator


class TestEdgeCases:
    def test_numbers_in_text(self, translator):
        result = translator.translate("hello 123", "en", "es")
        assert isinstance(result['target'], str)

    def test_special_characters(self, translator):
        result = translator.translate("hello! @world#", "en", "es")
        assert isinstance(result['target'], str)

    def test_very_long_text(self, translator):
        text = "hello " * 100
        result = translator.translate(text, "en", "es")
        assert isinstance(result['target'], str)

    def test_unicode_text(self, translator):
        result = translator.translate("café", "en", "es")
        assert isinstance(result['target'], str)

    def test_mixed_case(self, translator):
        r1 = translator.translate("HELLO", "en", "es")
        r2 = translator.translate("hello", "en", "es")
        assert isinstance(r1['target'], str)
        assert isinstance(r2['target'], str)


class TestErrorHandling:
    def test_invalid_source_language(self, translator):
        result = translator.translate("hello", "xx", "es")
        assert isinstance(result['target'], str)

    def test_invalid_target_language(self, translator):
        result = translator.translate("hello", "en", "xx")
        assert isinstance(result['target'], str)


class TestConsistency:
    def test_same_input_same_output(self, translator):
        r1 = translator.translate("hello", "en", "es")
        r2 = translator.translate("hello", "en", "es")
        assert r1['target'] == r2['target']
        assert r1['confidence'] == r2['confidence']


class TestRoundTrip:
    def test_roundtrip_english(self, translator):
        result = translator.translate("hello", "en", "en")
        assert result['confidence'] > 0.7

    def test_roundtrip_preserves_length_approximately(self, translator):
        result = translator.translate("hello", "en", "es")
        ratio = len(result['target']) / max(1, len(result['source']))
        assert 0.3 < ratio < 3.0
