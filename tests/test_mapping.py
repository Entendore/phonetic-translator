"""Tests for phoneme mapping."""
import pytest
from translator.mapping import PhonemeMapper


class TestPhonemeMapperInit:
    def test_creates_instance(self):
        assert PhonemeMapper() is not None


class TestGetInventory:
    def test_english_inventory(self, mapper):
        inv = mapper.get_inventory('en')
        assert isinstance(inv, list)
        assert len(inv) > 0
        assert 'p' in inv

    def test_unknown_language_returns_default(self, mapper):
        inv = mapper.get_inventory('xx')
        assert isinstance(inv, list)
        assert len(inv) > 0


class TestFindClosest:
    def test_exact_match(self, mapper):
        assert mapper.find_closest('p', 'en') == 'p'

    def test_returns_string(self, mapper):
        assert isinstance(mapper.find_closest('θ', 'es'), str)

    def test_returns_valid_phoneme(self, mapper):
        result = mapper.find_closest('θ', 'es')
        assert result in mapper.get_inventory('es')


class TestMapSequence:
    def test_basic_sequence(self, mapper):
        result = mapper.map_sequence(['h', 'ɛ', 'l', 'oʊ'], 'es')
        assert isinstance(result, list)
        assert len(result) == 4

    def test_empty_sequence(self, mapper):
        assert mapper.map_sequence([], 'es') == []

    def test_preserves_length(self, mapper):
        src = ['p', 'æ', 't']
        result = mapper.map_sequence(src, 'fr')
        assert len(result) == len(src)
