"""
Wylie Transliterator Package
A Domain-Driven Design implementation for Tibetan script transliteration.

Now with ACIP (Asian Classics Input Project) support!
"""

from .application.transliteration_service import TransliterationService
from .application.acip_service import ACIPService
from .domain.models.syllable import Syllable, SyllableComponents
from .domain.services.transliterator import WylieToTibetanTransliterator

__version__ = "2.1.0"
__all__ = [
    "TransliterationService",
    "ACIPService",
    "Syllable",
    "SyllableComponents",
    "WylieToTibetanTransliterator",
]

