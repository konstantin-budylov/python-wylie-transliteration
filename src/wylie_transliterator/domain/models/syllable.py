"""
Syllable Domain Model
Represents the structure of a Tibetan syllable according to EWTS specification.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SyllableComponents:
    """
    Value Object representing the 7 possible components of a Tibetan syllable.
    
    According to THL EWTS, a syllable has the structure:
    [prescript] [superscript] ROOT [subscript] [vowel] [postscript1] [postscript2]
    
    Attributes:
        prescript: Optional leading consonant (g, d, b, m, ')
        superscript: Optional top consonant (r, l, s)
        root: Required base consonant
        subscript: Optional bottom consonant (r, l, y, w) - can be double
        vowel: Vowel marker (a is inherent/default)
        postscript1: Optional first  final consonant
        postscript2: Optional second final consonant
    """
    root: str
    prescript: Optional[str] = None
    superscript: Optional[str] = None
    subscript: Optional[str] = None
    vowel: str = 'a'
    postscript1: Optional[str] = None
    postscript2: Optional[str] = None
    
    def __post_init__(self):
        """Validate syllable structure"""
        if not self.root:
            raise ValueError("Syllable must have a root consonant")


@dataclass
class Syllable:
    """
    Entity representing a complete Tibetan syllable.
    
    Combines the structural components with their Unicode representation.
    """
    components: SyllableComponents
    unicode_text: str
    wylie_text: str
    
    def __str__(self) -> str:
        return self.unicode_text
    
    def __repr__(self) -> str:
        return f"Syllable(wylie='{self.wylie_text}', unicode='{self.unicode_text}')"

