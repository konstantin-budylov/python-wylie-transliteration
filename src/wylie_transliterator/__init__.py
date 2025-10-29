"""
Wylie Transliterator Package
A Domain-Driven Design implementation for Tibetan script transliteration.
"""

from .application.transliteration_service import TransliterationService
from .domain.models.syllable import Syllable, SyllableComponents
from .domain.services.transliterator import WylieToTibetanTransliterator

__version__ = "2.0.0"
__all__ = [
    "TransliterationService",
    "Syllable",
    "SyllableComponents",
    "WylieToTibetanTransliterator",
]

