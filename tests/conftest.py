"""Shared test fixtures."""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from translator import PhoneticTranslator
from translator.mapping import PhonemeMapper
from translator.p2g import PhonemeToGrapheme


@pytest.fixture(scope="session")
def translator():
    return PhoneticTranslator()


@pytest.fixture(scope="session")
def mapper():
    return PhonemeMapper()


@pytest.fixture(scope="session")
def p2g():
    return PhonemeToGrapheme()


@pytest.fixture
def sample_translations():
    return [
        ("hello", "en", "es"),
        ("world", "en", "fr"),
        ("test", "en", "de"),
        ("goodbye", "en", "it"),
        ("thank you", "en", "ja"),
    ]
