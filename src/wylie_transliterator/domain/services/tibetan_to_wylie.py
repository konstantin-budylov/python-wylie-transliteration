"""
Tibetan to Wylie Transliterator Domain Service
Converts Tibetan Unicode to Extended Wylie transliteration.
"""

from typing import List, Tuple, Optional
from ..value_objects.reverse_mappings import ReverseCharacterMappings


class TibetanToWylieTransliterator:
    """
    Domain Service for Tibetan Unicode → Wylie transliteration.
    
    Design Principles:
    - Single Responsibility: Only reverse transliteration logic
    - DRY: Reuses reverse mappings
    - KISS: Simple character-by-character processing
    - Stateless: Each transliteration is independent
    
    Tibetan syllable structure (in Unicode order):
    1. Optional PRESCRIPT (base: g, d, b, m, ')
    2. Optional SUPERSCRIPT (base: r, l, s)
    3. ROOT (base if no superscript, or subjoined if superscript exists)
    4. Optional SUBSCRIPTS (subjoined: r, l, y, w, m)
    5. Optional VOWEL
    6. Optional POSTSCRIPTS (1-2 base consonants)
    7. Optional Sanskrit marks
    """
    
    # Valid prescripts
    PRESCRIPTS = {'g', 'd', 'b', 'm', "'"}
    
    # Valid superscripts  
    SUPERSCRIPTS = {'r', 'l', 's'}
    
    # Valid subscripts
    SUBSCRIPTS = {'r', 'l', 'y', 'w', 'm'}
    
    def __init__(self):
        """Initialize with reverse character mappings"""
        self.mappings = ReverseCharacterMappings()
    
    def transliterate(self, tibetan_text: str) -> str:
        """
        Transliterate Tibetan Unicode to Wylie.
        
        Args:
            tibetan_text: Tibetan Unicode text
        
        Returns:
            Extended Wylie transliteration
        
        Example:
            >>> trans = TibetanToWylieTransliterator()
            >>> trans.transliterate('བླ་མ')
            'bla ma'
        """
        if not tibetan_text:
            return ''
        
        result = []
        i = 0
        
        while i < len(tibetan_text):
            char = tibetan_text[i]
            
            # Check for tsheg (syllable separator) first
            if self.mappings.is_tsheg(char):
                result.append(' ')
                i += 1
                continue
            
            # Check for Tibetan numerals (U+0F20 - U+0F29)
            if '\u0F20' <= char <= '\u0F29':
                wylie = self.mappings.get_wylie(char)
                result.append(wylie if wylie else char)
                i += 1
                continue
            
            # Check for punctuation
            if self.mappings.is_punctuation(char):
                # Handle multi-char punctuation
                if char == '\u0F0E':  # Double shad
                    result.append('//')
                else:
                    wylie = self.mappings.get_wylie(char)
                    result.append(wylie if wylie else char)
                i += 1
                continue
            
            # Check for standalone Sanskrit marks (not part of syllable structure)
            if char in ['\u0F7E', '\u0F7F', '\u0F83']:
                wylie = self.mappings.get_wylie(char)
                result.append(wylie if wylie else char)
                i += 1
                continue
            
            # Check for special compound: kss (ཀྵ)
            if i + 1 < len(tibetan_text):
                compound = tibetan_text[i:i+2]
                wylie = self.mappings.get_wylie(compound)
                if wylie:
                    result.append(wylie)
                    i += 2
                    continue
            
            # Try to match syllable
            syllable_wylie, length = self._match_syllable(tibetan_text[i:])
            if syllable_wylie:
                result.append(syllable_wylie)
                i += length
            else:
                # Unknown character, keep as-is
                result.append(char)
                i += 1
        
        return ''.join(result)
    
    def _match_syllable(self, text: str) -> Tuple[str, int]:
        """
        Match a complete Tibetan syllable following proper Unicode structure.
        
        Structure:
        1. Prescript (optional): g, d, b, m, ' as BASE consonants
        2. Superscript (optional): r, l, s as BASE consonants
        3. Root: BASE consonant (or SUBJOINED if superscript exists)
        4. Subscripts (optional): SUBJOINED r, l, y, w, m
        5. Vowel (optional): vowel marks
        6. Postscripts (optional): 1-2 BASE consonants
        7. Sanskrit marks (optional)
        
        Returns:
            (wylie_string, length_matched)
        """
        if not text:
            return ('', 0)
        
        pos = 0
        parts = []
        has_explicit_vowel = False
        
        # Step 1: Try to match prescript (base consonant in PRESCRIPTS set)
        # Prescript only if followed by another BASE consonant (not subjoined)
        prescript = None
        if pos < len(text) and self.mappings.is_consonant(text[pos]):
            wylie = self.mappings.get_wylie(text[pos])
            if wylie:
                # Remove trailing 'a'
                if wylie.endswith('a') and len(wylie) > 1:
                    wylie_base = wylie[:-1]
                else:
                    wylie_base = wylie
                
                # Check if it's a prescript
                if wylie_base in self.PRESCRIPTS:
                    # Prescript only if followed by BASE consonant (not subjoined)
                    if pos + 1 < len(text) and self.mappings.is_consonant(text[pos+1]):
                        # Make sure next is NOT in subjoined range
                        if not ('\u0F90' <= text[pos+1] <= '\u0FBC'):
                            prescript = wylie_base
                            pos += 1
        
        # Step 2: Try to match superscript (base consonant in SUPERSCRIPTS set)
        superscript = None
        if pos < len(text) and self.mappings.is_consonant(text[pos]):
            wylie = self.mappings.get_wylie(text[pos])
            if wylie:
                # Remove trailing 'a'
                if wylie.endswith('a') and len(wylie) > 1:
                    wylie_base = wylie[:-1]
                else:
                    wylie_base = wylie
                
                # Check if it's a superscript
                if wylie_base in self.SUPERSCRIPTS:
                    # Look ahead to see if there's a subjoined (root) after
                    if pos + 1 < len(text) and '\u0F90' <= text[pos+1] <= '\u0FBC':
                        superscript = wylie_base
                        pos += 1
        
        # Step 3: Match root
        root = None
        if pos < len(text):
            char = text[pos]
            
            # If we have a superscript, root must be subjoined
            if superscript and '\u0F90' <= char <= '\u0FBC':
                wylie = self.mappings.get_wylie(char)
                if wylie:
                    root = wylie
                    pos += 1
            # Otherwise, root is a base consonant
            elif self.mappings.is_consonant(char):
                wylie = self.mappings.get_wylie(char)
                if wylie:
                    # Remove trailing 'a'
                    if wylie.endswith('a') and len(wylie) > 1:
                        root = wylie[:-1]
                    else:
                        root = wylie
                    pos += 1
        
        if not root:
            return ('', 0)
        
        # Step 4: Match subscripts (subjoined consonants)
        subscripts = []
        while pos < len(text):
            char = text[pos]
            # Check if it's in subjoined range
            if '\u0F90' <= char <= '\u0FBC':
                wylie = self.mappings.get_wylie(char)
                if wylie:
                    subscripts.append(wylie)
                    pos += 1
                else:
                    break
            else:
                break
        
        # Step 5: Match vowel
        vowel = None
        if pos < len(text):
            # Check for compound vowels first (2 chars)
            if pos + 1 < len(text):
                compound = text[pos:pos+2]
                wylie = self.mappings.get_wylie(compound)
                if wylie:
                    vowel = wylie
                    pos += 2
                    has_explicit_vowel = True
            
            # Try single vowel
            if not vowel and self.mappings.is_vowel(text[pos]):
                wylie = self.mappings.get_wylie(text[pos])
                if wylie and wylie != 'a':
                    vowel = wylie
                    has_explicit_vowel = True
                pos += 1
        
        # Step 6: Match postscripts (final consonants)
        postscripts = []
        while pos < len(text) and self.mappings.is_consonant(text[pos]):
            wylie = self.mappings.get_wylie(text[pos])
            if wylie:
                # Remove trailing 'a'
                if wylie.endswith('a') and len(wylie) > 1:
                    wylie = wylie[:-1]
                postscripts.append(wylie)
                pos += 1
            else:
                break
        
        # Step 7: Match Sanskrit marks
        marks = []
        while pos < len(text) and text[pos] in ['\u0F7E', '\u0F7F', '\u0F83']:
            wylie = self.mappings.get_wylie(text[pos])
            if wylie:
                marks.append(wylie)
                pos += 1
            else:
                break
        
        # Build final Wylie string
        result = []
        
        if prescript:
            result.append(prescript)
        if superscript:
            result.append(superscript)
        
        # Special case: vowel-initial syllable (root='a' with explicit vowel, no subscripts)
        # In EWTS, ཨོམ should be 'om' not 'aom'
        is_vowel_initial = (root == 'a' and has_explicit_vowel and not subscripts and not prescript and not superscript)
        
        if is_vowel_initial:
            # For vowel-initial syllables, skip the 'a' root entirely
            # e.g., ཨོམ → 'om' (just the vowel, not 'a' + vowel)
            result.append(vowel)
        else:
            # Root + subscripts
            root_part = root
            for sub in subscripts:
                root_part += sub
            
            # Add inherent 'a' to root if no explicit vowel and root isn't already 'a'
            if not has_explicit_vowel and root != 'a':
                root_part += 'a'
            
            result.append(root_part)
            
            if vowel:
                result.append(vowel)
        
        result.extend(postscripts)
        result.extend(marks)
        
        return (''.join(result), pos)
    
    def transliterate_batch(self, tibetan_texts: List[str]) -> List[str]:
        """
        Transliterate multiple Tibetan texts (DRY principle).
        
        Args:
            tibetan_texts: List of Tibetan Unicode texts
        
        Returns:
            List of Wylie transliterations
        
        Example:
            >>> trans = TibetanToWylieTransliterator()
            >>> trans.transliterate_batch(['བླ་མ', 'སངས་རྒྱས'])
            ['bla ma', 'sangs rgyas']
        """
        return [self.transliterate(text) for text in tibetan_texts]
