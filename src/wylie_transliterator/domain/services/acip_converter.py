"""
ACIP Converter Domain Service
Handles conversion logic between ACIP and EWTS transliteration systems.
"""

import re
from typing import List
from ..value_objects.acip_mappings import (
    ACIPAlphabet,
    ACIPPatterns,
    ACIPStandardStacks
)


class ACIPConverter:
    """
    Domain Service for converting between ACIP and EWTS.
    
    ACIP (Asian Classics Input Project) is a transliteration system
    widely used for digitizing Tibetan Buddhist texts. This converter
    provides bidirectional conversion with EWTS.
    
    Conversion Flow:
    - ACIP → EWTS → Tibetan Unicode (using existing EWTS converter)
    - Tibetan Unicode → EWTS → ACIP (using existing EWTS converter)
    """
    
    def __init__(self):
        self._alphabet = ACIPAlphabet()
        self._patterns = ACIPPatterns()
        self._stacks = ACIPStandardStacks()
    
    def acip_to_ewts(self, acip_text: str) -> str:
        """
        Convert ACIP transliteration to EWTS.
        
        Args:
            acip_text: Input text in ACIP format
            
        Returns:
            Text in EWTS format
            
        Example:
            >>> converter = ACIPConverter()
            >>> converter.acip_to_ewts("BSGRUBS")
            'bsgrubs'
            >>> converter.acip_to_ewts("BA'I")
            'ba'i'
        """
        result = acip_text
        
        # Step 1: Remove ACIP comments
        result = self._remove_comments(result)
        
        # Step 2: Remove parentheses (yichung markers in ACIP)
        result = result.replace('(', '').replace(')', '')
        
        # Step 3: Convert ACIP parentheses notation to EWTS
        # /.../ in ACIP = (...) in EWTS
        result = self._patterns.PARENS.sub(r'(\1)', result)
        result = result.replace('/', '')  # Remove remaining slashes
        
        # Step 4: Convert simple punctuation
        result = self._convert_simple_punctuation(result)
        
        # Step 5: Handle special characters
        result = self._convert_special_characters(result)
        
        # Step 6: Handle TS/TZ distinction
        # Must do this before case conversion!
        result = self._handle_ts_tz(result)
        
        # Step 7: Handle dots for GA-YAS pattern
        result = self._convert_dots(result)
        
        # Step 8: Handle vowel conversions
        result = self._convert_vowels(result)
        
        # Step 9: Handle consonant + vowel patterns
        result = self._handle_consonant_vowel_patterns(result)
        
        # Step 10: Handle special 'sh' case
        result = self._handle_sh_pattern(result)
        
        # Step 11: Normalize apostrophes
        result = self._normalize_apostrophes(result)
        
        # Step 12: Swap case (ACIP uses uppercase, EWTS uses lowercase)
        result = result.swapcase()
        
        # Step 13: Final vowel conversions (after case swap)
        result = self._convert_final_vowels(result)
        
        # Step 14: Add + for stacks where needed
        result = self._add_plus_for_stacks(result)
        
        # Step 15: Normalize spaces (tsheg vs space)
        result = self._normalize_spaces(result)
        
        return result
    
    def ewts_to_acip(self, ewts_text: str) -> str:
        """
        Convert EWTS transliteration to ACIP.
        
        Args:
            ewts_text: Input text in EWTS format
            
        Returns:
            Text in ACIP format
            
        Example:
            >>> converter = ACIPConverter()
            >>> converter.ewts_to_acip("bsgrubs")
            'BSGRUBS'
            >>> converter.ewts_to_acip("ba'i")
            'BA'I'
        """
        result = ewts_text
        
        # Step 1: Normalize apostrophes
        result = self._normalize_apostrophes(result)
        
        # Step 2: Convert parentheses notation
        # (...) in EWTS = /.../ in ACIP
        result = re.sub(r'\(([^)]*)\)', r'/\1/', result)
        
        # Step 3: Convert simple punctuation (reverse)
        result = self._convert_punctuation_to_acip(result)
        
        # Step 4: Convert special characters
        result = self._convert_special_to_acip(result)
        
        # Step 5: Handle ts/tsh → TZ/TS conversion (before case swap!)
        result = self._handle_ewts_ts_to_acip(result)
        
        # Step 6: Handle 'w' → 'v' in ACIP
        result = result.replace('w', 'v')
        
        # Step 7: Swap case (EWTS lowercase → ACIP uppercase)
        result = result.swapcase()
        
        # Step 8: Handle vowel conversions
        result = self._convert_vowels_to_acip(result)
        
        # Step 9: Handle dots
        result = result.replace('.', '-')
        
        # Step 10: Handle ai/au
        result = result.replace('AI', 'EE')
        result = result.replace('AU', 'OO')
        
        # Step 11: Add 'A' for independent vowels
        result = self._add_a_for_independent_vowels(result)
        
        # Step 12: Handle lowercase vowels after apostrophe
        result = self._handle_apostrophe_vowels_acip(result)
        
        # Step 13: Handle special 'sh' case (reverse)
        result = result.replace('sH', 'sh')
        
        return result
    
    def _remove_comments(self, text: str) -> str:
        """Remove ACIP comments: @... and [...]"""
        text = self._patterns.COMMENT_BRACKET.sub('', text)
        text = self._patterns.COMMENT_AT.sub('', text)
        return text
    
    def _convert_simple_punctuation(self, text: str) -> str:
        """Convert simple ACIP punctuation to EWTS."""
        text = text.replace(';', '|')
        text = text.replace('#', '@##')  # Temporary marker
        # Handle asterisks
        text = self._patterns.ASTERISK_ENCODING.sub(
            lambda m: '@' + '#' * len(m.group(0)),
            text
        )
        text = text.replace('\\', '?')
        text = text.replace(',', '/')
        text = text.replace('`', '!')
        return text
    
    def _convert_special_characters(self, text: str) -> str:
        """Convert special ACIP characters."""
        text = text.replace('^', '\\u0F38')
        text = text.replace('%', '~x')
        text = text.replace('V', 'W')  # ACIP V = EWTS w
        return text
    
    def _handle_ts_tz(self, text: str) -> str:
        """Handle TS/TZ distinction before case conversion."""
        # ACIP TS = EWTS tsh
        # ACIP TZ = EWTS ts
        # Use placeholders to avoid confusion
        text = text.replace('TS', 'ZZZ')  # Temporary
        text = text.replace('TZ', 'TS')   # TZ → ts
        text = text.replace('ZZZ', 'TSH') # TS → tsh
        return text
    
    def _convert_dots(self, text: str) -> str:
        """Convert GA-YAS pattern dots."""
        # GA-YAS in ACIP = g.yas in EWTS
        text = self._patterns.GA_YAS_PATTERN.sub(r'\1.', text)
        text = text.replace('-', '.')
        return text
    
    def _convert_vowels(self, text: str) -> str:
        """Convert ACIP vowels (before case swap)."""
        # Handle special vowel patterns
        text = re.sub(r'A?i', '-I', text)  # Ai or i → -I
        text = re.sub(r"A?'-I", '-i', text)  # A'i or 'i → -i
        text = text.replace('o', 'x')  # Temporary marker
        return text
    
    def _handle_consonant_vowel_patterns(self, text: str) -> str:
        """Handle consonant + apostrophe + vowel patterns."""
        # B'I in ACIP = bi in EWTS
        text = self._patterns.VOWEL_AFTER_CONS.sub(
            lambda m: m.group(1) + m.group(2).lower(),
            text
        )
        # Special case: A is main letter
        text = re.sub(
            r"(^|[^BCDGHJKLMNPR'STWYZhdtn])A'([AEOUI])",
            lambda m: m.group(1) + m.group(2).lower(),
            text
        )
        # A + vowel → vowel
        text = re.sub(r'A([AEIOUaeiou])', r'\1', text)
        return text
    
    def _handle_sh_pattern(self, text: str) -> str:
        """Handle special 'sh' patterns."""
        # In ACIP: sh (lowercase) = Sanskrit Sh
        # In ACIP: SH (uppercase) = regular sh
        # Before case swap, convert sh → sH temporarily
        text = text.replace('sh', 'sH')
        return text
    
    def _normalize_apostrophes(self, text: str) -> str:
        """Normalize different apostrophe characters."""
        text = re.sub(r"['ʼʹ'ʾ]", "'", text)
        return text
    
    def _convert_final_vowels(self, text: str) -> str:
        """Convert vowels after case swap."""
        text = text.replace('ee', 'ai')
        text = text.replace('oo', 'au')
        text = text.replace(':', 'H')
        return text
    
    def _add_plus_for_stacks(self, text: str) -> str:
        """Add + signs for non-standard stacks (Sanskrit, etc.)."""
        def process_consonants(match):
            consonants = match.group(1)
            vowel = match.group(2)
            
            # Skip if there's already a + sign (explicit Sanskrit notation)
            if '+' in consonants:
                return consonants + vowel
            
            # Check if this is a standard Tibetan stack
            if self._stacks.is_valid_stack(consonants):
                return consonants + vowel
            
            # Not a standard stack, need to add + signs
            # Tokenize consonants
            tokens = self._tokenize_consonants(consonants)
            
            if len(tokens) == 1:
                return consonants + vowel
            
            # Check if first two tokens form a valid stack with prefix
            if len(tokens) >= 2:
                first_two = tokens[0] + tokens[1]
                if first_two.lower() in [s.lower() for s in ACIPStandardStacks.STD_TIB_STACKS_PREFIX]:
                    # First token is prefix, rest need +
                    return tokens[0] + '+'.join(tokens[1:]) + vowel
            
            # All consonants need + between them
            return '+'.join(tokens) + vowel
        
        # Apply to consonant sequences before vowels
        # Modified pattern to include + in consonant groups
        pattern = re.compile(r"([bcdgjklm'nprstwyzhSDTN+]+)([aeiouAEIOU.-])")
        text = pattern.sub(process_consonants, text)
        return text
    
    def _tokenize_consonants(self, consonants: str) -> List[str]:
        """Tokenize consonant string into individual letters/digraphs."""
        # Multi-character tokens (must check longest first)
        multi_tokens = ['zh', 'ny', 'dz', 'ts', 'tsh', 'ch', 'ph', 'th', 
                       'sh', 'Sh', 'kh', 'ng']
        single_chars = 'NDTRYWbcdghjklmnprstwyz\''
        
        result = []
        i = 0
        while i < len(consonants):
            matched = False
            # Try multi-character tokens
            for token in multi_tokens:
                if consonants[i:].startswith(token):
                    result.append(token)
                    i += len(token)
                    matched = True
                    break
            
            if not matched:
                # Single character
                if i < len(consonants) and consonants[i] in single_chars:
                    result.append(consonants[i])
                i += 1
        
        return result
    
    def _normalize_spaces(self, text: str) -> str:
        """Normalize spaces in EWTS (space vs underscore for tsheg)."""
        # In context where space should be tsheg, use space
        # Where actual space needed, it should be underscore
        text = self._patterns.SPACE_BEFORE_PUNCT.sub(
            lambda m: m.group(1) + '_' + m.group(2),
            text
        )
        text = self._patterns.SPACE_AFTER_PUNCT.sub(
            lambda m: m.group(1) + '_',
            text
        )
        return text
    
    def _convert_punctuation_to_acip(self, text: str) -> str:
        """Convert EWTS punctuation to ACIP."""
        text = text.replace('|', ';')
        # Remove * not after [
        text = re.sub(r'(^|\[)\*', lambda m: m.group(1), text)
        text = text.replace('@##', 'ZZ')  # Temporary
        text = text.replace('@#', '*')
        text = text.replace('_', ' ')
        # Remove # not after [
        text = re.sub(r'(^|\[)#', lambda m: m.group(1), text)
        text = text.replace('ZZ', '#')
        text = text.replace('?', '\\')
        text = text.replace('/', ',')
        text = text.replace('!', '`')
        return text
    
    def _convert_special_to_acip(self, text: str) -> str:
        """Convert special EWTS characters to ACIP."""
        text = re.sub(r'\\U0F38', '^', text, flags=re.I)
        text = text.replace('~X', '%')
        text = text.replace('H', ':')
        return text
    
    def _handle_ewts_ts_to_acip(self, text: str) -> str:
        """Handle EWTS ts/tsh to ACIP TZ/TS conversion."""
        # EWTS tsh = ACIP TS
        # EWTS ts = ACIP TZ
        text = text.replace('tsh', 'ZZZ')  # Temporary
        text = text.replace('ts', 'tz')
        text = text.replace('ZZZ', 'ts')
        return text
    
    def _convert_vowels_to_acip(self, text: str) -> str:
        """Convert EWTS vowels to ACIP (after case swap)."""
        # The vowels are swapped at this point
        text = text.replace('-I', 'w')  # Will become 'i' after final conversion
        text = text.replace('-i', 'q')  # Will become 'i after final conversion
        return text
    
    def _add_a_for_independent_vowels(self, text: str) -> str:
        """Add 'A' prefix for independent vowels in ACIP."""
        # In ACIP, independent vowels need 'A' prefix
        text = re.sub(
            r"(^|[^BCDGHJKLMNPR'STVYZhdtnEO])([AEOUIqaewiou])",
            lambda m: m.group(1) + 'A' + m.group(2),
            text
        )
        return text
    
    def _handle_apostrophe_vowels_acip(self, text: str) -> str:
        """Handle vowels after apostrophes in ACIP."""
        text = text.replace('a', "'A")
        text = text.replace('u', "'U")
        text = text.replace('o', "'O")
        text = text.replace('e', "'E")
        text = text.replace('i', "'I")
        text = text.replace('q', "'i")  # From earlier conversion
        text = text.replace('w', 'i')   # From earlier conversion
        text = text.replace('x', 'o')   # From temporary marker
        return text

