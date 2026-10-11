"""Tests for all 10 use cases."""
import pytest
from translator import PhoneticTranslator


class TestPronunciationTutor:
    def test_perfect_pronunciation(self, translator):
        t_ipa = translator.text_to_ipa("hello", "en")
        s_ipa = translator.text_to_ipa("hello", "en")
        t_ph = translator.ipa_to_phonemes(t_ipa)
        s_ph = translator.ipa_to_phonemes(s_ipa)
        mismatches = sum(1 for a, b in zip(t_ph, s_ph) if a != b)
        assert mismatches == 0

    def test_mismatch_detected(self, translator):
        t_ipa = translator.text_to_ipa("think", "en")
        s_ipa = translator.text_to_ipa("sink", "en")
        t_ph = translator.ipa_to_phonemes(t_ipa)
        s_ph = translator.ipa_to_phonemes(s_ipa)
        mismatches = sum(1 for a, b in zip(t_ph, s_ph) if a != b)
        assert mismatches > 0


class TestProductNameValidator:
    def test_simple_name(self, translator):
        result = translator.translate("Nova", "en", "es")
        assert result['confidence'] > 0.5

    @pytest.mark.parametrize("name", ["Apple", "Nike", "Sony", "Zara"])
    def test_real_brands(self, translator, name):
        for lang in ['es', 'fr', 'de']:
            result = translator.translate(name, "en", lang)
            assert len(result['target']) > 0


class TestTTSPreprocessor:
    def test_basic_preprocessing(self, translator):
        ipa = translator.text_to_ipa("hello world", "en")
        assert isinstance(ipa, str)
        assert len(ipa) > 0


class TestHashtagGenerator:
    def test_hashtag_format(self, translator):
        result = translator.translate("good vibes", "en", "es")
        hashtag = '#' + ''.join(c for c in result['tgt_ipa'] if c.isalnum())
        assert hashtag.startswith('#')


class TestNPCNameGenerator:
    @pytest.mark.parametrize("name", ["Thalion", "Zephyra", "Kaelith"])
    def test_fantasy_names_pronounceable(self, translator, name):
        for lang in ['es', 'fr', 'de']:
            result = translator.translate(name, "en", lang)
            assert result['confidence'] > 0.3


class TestLyricTranslator:
    def test_syllable_counting(self, translator):
        ipa = translator.text_to_ipa("hello", "en")
        phonemes = translator.ipa_to_phonemes(ipa)
        vowels = set('iɪeɛæaɑɔoʊuʌə')
        syllable_count = sum(1 for p in phonemes if p in vowels)
        assert syllable_count >= 1


class TestTravelPhraseGuide:
    @pytest.mark.parametrize("phrase", ["Hello", "Thank you", "Please"])
    def test_travel_phrases(self, translator, phrase):
        for lang in ['es', 'fr', 'de']:
            result = translator.translate(phrase, "en", lang)
            assert len(result['target']) > 0


class TestBrandNameTester:
    @pytest.mark.parametrize("brand", ["Nova", "Apex", "Luma"])
    def test_brand_names(self, translator, brand):
        results = []
        for lang in ['es', 'fr', 'de', 'ja']:
            r = translator.translate(brand, "en", lang)
            results.append(r['confidence'])
        assert any(c > 0.5 for c in results)


class TestAccentAdaptiveAssistant:
    def test_command_matching(self, translator):
        correct = translator.text_to_ipa("turn on the lights", "en")
        accented = translator.text_to_ipa("torn on the lights", "en")
        correct_ph = translator.ipa_to_phonemes(correct)
        accented_ph = translator.ipa_to_phonemes(accented)
        common = sum(1 for a, b in zip(correct_ph, accented_ph) if a == b)
        similarity = common / max(len(correct_ph), len(accented_ph))
        assert similarity > 0.5


class TestSubtitleHelper:
    @pytest.mark.parametrize("word", ["croissant", "bruschetta"])
    def test_foreign_word_pronunciation(self, translator, word):
        ipa = translator.text_to_ipa(word, "en")
        assert isinstance(ipa, str)
        assert len(ipa) > 0
