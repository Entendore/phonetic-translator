"""
Phonetic Translator - Translate text between languages via phonetic transcription.
"""
from .core import PhoneticTranslator
from .mapping import PhonemeMapper
from .p2g import PhonemeToGrapheme

__version__ = "1.0.0"
__all__ = ["PhoneticTranslator", "PhonemeMapper", "PhonemeToGrapheme"]
