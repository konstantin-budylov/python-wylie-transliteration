"""
Reverse Character Mappings (Tibetan Unicode → Wylie)
Value object for reverse transliteration following DRY principle.
"""

from typing import Dict
from .character_mappings import TibetanAlphabet


class ReverseCharacterMappings:
    """
    Immutable reverse mappings from Tibetan Unicode to Wylie.
    
    Design Principles:
    - DRY: Generated from existing TibetanAlphabet mappings
    - KISS: Simple dictionary lookups
    - Immutable: Mappings cannot be modified
    """
    
    def __init__(self):
        """Initialize reverse mappings from TibetanAlphabet"""
        alphabet = TibetanAlphabet()
        
        # Reverse consonants mapping
        self._consonants = self._reverse_dict(alphabet.CONSONANTS)
        
        # Reverse vowels mapping
        self._vowels = self._reverse_dict(alphabet.VOWELS)
        
        # Reverse subscripts mapping
        self._subscripts = self._reverse_dict(alphabet.SUBSCRIPTS)
        
        # Reverse punctuation mapping
        self._punctuation = self._reverse_dict(alphabet.PUNCTUATION)
        
        # Reverse Sanskrit marks mapping
        self._sanskrit_marks = self._reverse_dict(alphabet.SANSKRIT_MARKS)
        
        # Reverse numerals mapping
        self._numerals = self._reverse_dict(alphabet.NUMERALS)
        
        # Reverse Sanskrit retroflex mapping
        self._sanskrit_retroflex = self._reverse_dict(alphabet.SANSKRIT_RETROFLEX)
        
        # Add subjoined consonant forms (U+0F90-0FBC)
        # These are base consonants + 0x50
        self._subjoined_consonants = {}
        for wylie, unicode_char in alphabet.CONSONANTS.items():
            base_code = ord(unicode_char)
            if 0x0F40 <= base_code <= 0x0F6C:  # Main consonant range
                subjoined_code = base_code + 0x50
                subjoined_char = chr(subjoined_code)
                # Remove 'a' from wylie if present
                wylie_no_a = wylie[:-1] if wylie.endswith('a') and len(wylie) > 1 else wylie
                self._subjoined_consonants[subjoined_char] = wylie_no_a
        
        # Build combined lookup for fast access
        self._all_chars = {}
        self._all_chars.update(self._consonants)
        self._all_chars.update(self._vowels)
        self._all_chars.update(self._subscripts)
        self._all_chars.update(self._punctuation)
        self._all_chars.update(self._sanskrit_marks)
        self._all_chars.update(self._numerals)
        self._all_chars.update(self._sanskrit_retroflex)
        self._all_chars.update(self._subjoined_consonants)
        
        # Special handling for compound vowels
        # U+0F71 U+0F74 (long a + u) → U
        compound_U = '\u0F71\u0F74'
        if compound_U not in self._all_chars:
            self._vowels[compound_U] = 'U'
            self._all_chars[compound_U] = 'U'
        
        # Special handling for alternative anusvara
        alt_anusvara = '\u0F83'
        if alt_anusvara not in self._all_chars:
            self._sanskrit_marks[alt_anusvara] = 'M'
            self._all_chars[alt_anusvara] = 'M'
        
        # Special handling for kss (ཀྵ = ka + subjoined ssa)
        kssa = '\u0F40\u0FB5'
        self._consonants[kssa] = 'kss'
        self._all_chars[kssa] = 'kss'
    
    def _reverse_dict(self, mapping: Dict[str, str]) -> Dict[str, str]:
        """
        Reverse a dictionary mapping (DRY principle).
        
        For conflicts (multiple Wylie → same Unicode), keeps shorter Wylie form.
        Example: 'v' and 'w' both map to same subscript, keep 'w' (shorter/standard)
        """
        reversed_map = {}
        for wylie, unicode_char in mapping.items():
            if unicode_char not in reversed_map or len(wylie) < len(reversed_map[unicode_char]):
                reversed_map[unicode_char] = wylie
        return reversed_map
    
    @property
    def consonants(self) -> Dict[str, str]:
        """Tibetan consonants (Unicode → Wylie)"""
        return self._consonants.copy()
    
    @property
    def vowels(self) -> Dict[str, str]:
        """Tibetan vowels (Unicode → Wylie)"""
        return self._vowels.copy()
    
    @property
    def subscripts(self) -> Dict[str, str]:
        """Tibetan subscripts (Unicode → Wylie)"""
        return self._subscripts.copy()
    
    @property
    def punctuation(self) -> Dict[str, str]:
        """Tibetan punctuation (Unicode → Wylie)"""
        return self._punctuation.copy()
    
    @property
    def sanskrit_marks(self) -> Dict[str, str]:
        """Sanskrit marks (Unicode → Wylie)"""
        return self._sanskrit_marks.copy()
    
    @property
    def numerals(self) -> Dict[str, str]:
        """Tibetan numerals (Unicode → Wylie)"""
        return self._numerals.copy()
    
    @property
    def all_characters(self) -> Dict[str, str]:
        """All character mappings combined (Unicode → Wylie)"""
        return self._all_chars.copy()
    
    def get_wylie(self, unicode_char: str) -> str:
        """
        Get Wylie representation for a Unicode character.
        
        Args:
            unicode_char: Tibetan Unicode character or sequence
        
        Returns:
            Wylie representation, or empty string if not found
        
        Example:
            >>> mappings = ReverseCharacterMappings()
            >>> mappings.get_wylie('ཀ')  # 'ka'
            >>> mappings.get_wylie('ི')  # 'i'
        """
        # Try compound characters first (multi-char Unicode sequences)
        if len(unicode_char) > 1 and unicode_char in self._all_chars:
            return self._all_chars[unicode_char]
        
        # Try single character
        return self._all_chars.get(unicode_char, '')
    
    def is_consonant(self, unicode_char: str) -> bool:
        """Check if character is a Tibetan consonant"""
        return unicode_char in self._consonants
    
    def is_vowel(self, unicode_char: str) -> bool:
        """Check if character is a Tibetan vowel"""
        return unicode_char in self._vowels
    
    def is_subscript(self, unicode_char: str) -> bool:
        """Check if character is a subscript"""
        return unicode_char in self._subscripts
    
    def is_punctuation(self, unicode_char: str) -> bool:
        """Check if character is punctuation"""
        return unicode_char in self._punctuation
    
    def is_tsheg(self, unicode_char: str) -> bool:
        """Check if character is tsheg (syllable separator)"""
        return unicode_char == '\u0F0B'  # TIBETAN MARK INTERSYLLABIC TSHEG

