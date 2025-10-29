"""
Syllable Builder Domain Service
Converts syllable components to Tibetan Unicode representation.
"""

from ..models.syllable import SyllableComponents, Syllable
from ..value_objects.character_mappings import TibetanAlphabet


class SyllableBuilder:
    """
    Domain Service for building Tibetan Unicode syllables from components.
    Follows EWTS specification for character ordering and combinations.
    """
    
    def __init__(self):
        self.alphabet = TibetanAlphabet()
    
    def build_syllable(self, components: SyllableComponents, wylie_text: str) -> Syllable:
        """
        Build a complete Tibetan syllable from its components.
        
        Args:
            components: Parsed syllable components
            wylie_text: Original Wylie text
            
        Returns:
            Complete Syllable entity with Unicode representation
        """
        unicode_parts = []
        
        # 1. Prescript
        if components.prescript:
            unicode_parts.append(self.alphabet.CONSONANTS.get(components.prescript, ''))
        
        # 2. Superscript
        if components.superscript:
            unicode_parts.append(self.alphabet.CONSONANTS.get(components.superscript, ''))
        
        # 3. Root (use subjoined if superscript exists)
        if components.superscript:
            unicode_parts.append(self.alphabet.SUBJOINED.get(components.root, ''))
        else:
            unicode_parts.append(self.alphabet.CONSONANTS.get(components.root, ''))
        
        # 4. Subscript (handle double subscripts like 'r+w')
        if components.subscript:
            if '+' in components.subscript:
                # Double subscript
                subs = components.subscript.split('+')
                for sub in subs:
                    unicode_parts.append(self.alphabet.SUBSCRIPTS.get(sub, ''))
            else:
                unicode_parts.append(self.alphabet.SUBSCRIPTS.get(components.subscript, ''))
        
        # 5. Vowel (skip inherent 'a')
        if components.vowel and components.vowel != 'a':
            unicode_parts.append(self.alphabet.VOWELS.get(components.vowel, ''))
        
        # 6. Postscript 1
        if components.postscript1:
            unicode_parts.append(self.alphabet.CONSONANTS.get(components.postscript1, ''))
        
        # 7. Postscript 2
        if components.postscript2:
            unicode_parts.append(self.alphabet.CONSONANTS.get(components.postscript2, ''))
        
        unicode_text = ''.join(unicode_parts)
        
        return Syllable(
            components=components,
            unicode_text=unicode_text,
            wylie_text=wylie_text
        )

