"""
Syllable Parser Domain Service
Parses Wylie text into syllable components using multi-strategy approach.
"""

from typing import Optional
from ..models.syllable import SyllableComponents
from ..value_objects.character_mappings import TibetanAlphabet, SyllableRules


class SyllableParsingStrategy:
    """Strategy interface for different parsing approaches"""
    
    def __init__(self):
        self.alphabet = TibetanAlphabet()
        self.rules = SyllableRules()
    
    def parse(self, text: str, strategy_name: str) -> tuple[Optional[SyllableComponents], int]:
        """Parse text using specified strategy, return (components, length_matched)"""
        raise NotImplementedError


class MultiStrategySyllableParser(SyllableParsingStrategy):
    """
    Domain Service for parsing Wylie syllables using multiple strategies.
    Implements greedy longest-match parsing with lookahead for ambiguous cases.
    """
    
    def parse_syllable(self, text: str) -> Optional[SyllableComponents]:
        """
        Parse Wylie text into syllable components.
        Tries multiple strategies and picks the longest valid match.
        """
        if not text:
            return None
        
        best_components = None
        best_length = 0
        
        # Try different parsing strategies in order
        strategies = ['simple', 'with_super', 'with_pre', 'full']
        
        for strategy in strategies:
            components, length = self._try_strategy(text, strategy)
            if components and length > best_length:
                best_length = length
                best_components = components
        
        return best_components
    
    def _try_strategy(self, text: str, strategy: str) -> tuple[Optional[SyllableComponents], int]:
        """Try a specific parsing strategy"""
        pos = 0
        prescript = None
        superscript = None
        root = None
        subscript = None
        vowel = 'a'
        postscript1 = None
        postscript2 = None
        
        # Strategy 1: Simple (root + modifiers only)
        if strategy == 'simple':
            pass  # Skip to root matching
        
        # Strategy 2: With prescript
        elif strategy == 'with_pre':
            prescript, pre_len = self._match_prescript(text[pos:])
            if prescript:
                pos += pre_len
        
        # Strategy 3: With superscript
        elif strategy in ['with_super', 'full']:
            if strategy == 'full':
                prescript, pre_len = self._match_prescript(text[pos:])
                if prescript:
                    pos += pre_len
            
            superscript, sup_len = self._match_superscript(text[pos:])
            if superscript:
                pos += sup_len
        
        # Match root (required)
        root, root_len = self._match_root(text[pos:])
        vowel = None  # Will be set below
        is_vowel_initial = False  # Track if this is a vowel-initial syllable
        
        if not root:
            # Check if syllable starts with a vowel (vowel-initial syllable)
            vowel, vowel_len = self._match_vowel(text[pos:])
            if vowel and vowel != 'a':
                # Vowel-initial syllable: use 'a' as implicit root
                root = 'a'
                pos += vowel_len  # Advance past the vowel we just matched
                is_vowel_initial = True
            else:
                return None, 0
        else:
            pos += root_len
        
        # Validate superscript + root combination
        if superscript:
            if not self._is_valid_superscript_combination(superscript, root):
                # Invalid combination, reject this parse
                return None, 0
        
        # Match subscript (can be double) - only for non-vowel-initial syllables
        subscript = None
        if not is_vowel_initial:
            subscript, sub_len = self._match_subscript(text[pos:])
            if subscript:
                pos += sub_len
        
        # Match vowel (only if not already matched above for vowel-initial syllables)
        if vowel is None:
            vowel, vowel_len = self._match_vowel(text[pos:])
            if vowel:
                pos += vowel_len
            else:
                vowel = 'a'  # Default inherent vowel
        
        # Match postscript 1
        postscript1, post1_len = self._match_postscript(text[pos:])
        if postscript1:
            pos += post1_len
            
            # Match postscript 2 if postscript1 exists
            postscript2, post2_len = self._match_postscript(text[pos:])
            if postscript2:
                pos += post2_len
        
        try:
            components = SyllableComponents(
                root=root,
                prescript=prescript,
                superscript=superscript,
                subscript=subscript,
                vowel=vowel,
                postscript1=postscript1,
                postscript2=postscript2
            )
            return components, pos
        except ValueError:
            return None, 0
    
    def _match_prescript(self, text: str) -> tuple[Optional[str], int]:
        """Match prescript, checking for multi-char consonant lookahead"""
        for pre in sorted(self.rules.PRESCRIPTS, key=len, reverse=True):
            if text.lower().startswith(pre):
                # Check if remainder could be multi-char consonant
                remainder = text[len(pre):]
                if self._could_be_multichar_consonant(remainder):
                    continue
                
                # Look ahead for valid root
                if self._has_valid_root_ahead(remainder):
                    return pre, len(pre)
        return None, 0
    
    def _match_superscript(self, text: str) -> tuple[Optional[str], int]:
        """Match superscript, checking for multi-char consonant lookahead"""
        for sup in sorted(self.rules.SUPERSCRIPTS, key=len, reverse=True):
            if text.lower().startswith(sup):
                remainder = text[len(sup):]
                if self._could_be_multichar_consonant(remainder):
                    continue
                if self._has_valid_root_ahead(remainder):
                    return sup, len(sup)
        return None, 0
    
    def _match_root(self, text: str) -> tuple[Optional[str], int]:
        """Match root consonant (longest first, preserving case for Sanskrit)"""
        # First try case-sensitive match for Sanskrit retroflexes
        for root in sorted(self.alphabet.CONSONANTS.keys(), key=len, reverse=True):
            if text.startswith(root):
                return root, len(root)
        
        # Then try case-insensitive match for regular consonants
        for root in sorted(self.alphabet.CONSONANTS.keys(), key=len, reverse=True):
            if text.lower().startswith(root.lower()):
                return root.lower(), len(root)
        return None, 0
    
    def _match_subscript(self, text: str) -> tuple[Optional[str], int]:
        """
        Match subscript (can be double like 'r+w')
        Also handles explicit + notation for Sanskrit stacks (e.g., 'n+D')
        """
        subscripts_matched = []
        pos = 0
        
        # Check for explicit + notation (Sanskrit stacks)
        if text.startswith('+'):
            pos += 1  # Skip the +
            # Match any consonant from SUBJOINED as subscript
            for cons in sorted(self.alphabet.SUBJOINED.keys(), key=len, reverse=True):
                if text[pos:].startswith(cons):  # Case-sensitive for Sanskrit
                    subscripts_matched.append(cons)
                    pos += len(cons)
                    
                    # Check for another + (double subscript)
                    if pos < len(text) and text[pos] == '+':
                        pos += 1
                        for cons2 in sorted(self.alphabet.SUBJOINED.keys(), key=len, reverse=True):
                            if text[pos:].startswith(cons2):
                                subscripts_matched.append(cons2)
                                pos += len(cons2)
                                break
                    break
            
            if subscripts_matched:
                return '+'.join(subscripts_matched), pos
            return None, 0
        
        # Standard implicit subscripts (r, l, y, w)
        for sub in sorted(self.alphabet.SUBSCRIPTS.keys(), key=len, reverse=True):
            if text[pos:].lower().startswith(sub):
                subscripts_matched.append(sub)
                pos += len(sub)
                
                # Try to match second subscript
                for sub2 in sorted(self.alphabet.SUBSCRIPTS.keys(), key=len, reverse=True):
                    if text[pos:].lower().startswith(sub2):
                        subscripts_matched.append(sub2)
                        pos += len(sub2)
                        break
                break
        
        if subscripts_matched:
            if len(subscripts_matched) > 1:
                return '+'.join(subscripts_matched), pos
            return subscripts_matched[0], pos
        return None, 0
    
    def _match_vowel(self, text: str) -> tuple[Optional[str], int]:
        """Match vowel sign"""
        for vowel in sorted(self.alphabet.VOWELS.keys(), key=len, reverse=True):
            if text.startswith(vowel):
                return vowel, len(vowel)
        return None, 0
    
    def _is_valid_superscript_combination(self, superscript: str, root: str) -> bool:
        """
        Validate that the superscript + root combination is valid in Tibetan orthography.
        
        In Tibetan, superscripts can only appear with specific root consonants:
        - r: can go with k, g, ng, j, ny, t, d, n, b, m, ts, dz
        - l: can go with k, g, ng, c, j, t, d, p, b
        - s: can go with k, g, ng, ny, t, d, n, p, b, m, ts
        """
        if not hasattr(self.rules, 'VALID_SUPERSCRIPT_COMBINATIONS'):
            # If rules don't have validation, allow all (backward compatibility)
            return True
        
        valid_roots = self.rules.VALID_SUPERSCRIPT_COMBINATIONS.get(superscript, [])
        return root in valid_roots
    
    def _match_postscript(self, text: str) -> tuple[Optional[str], int]:
        """Match postscript consonant (capitals signal new syllable, not postscripts)"""
        # Don't match if starting with capital (Sanskrit consonant starts new syllable)
        if text and text[0].isupper():
            return None, 0
        
        for post in sorted(self.rules.POSTSCRIPTS, key=len, reverse=True):
            if text.lower().startswith(post):
                # Special case: apostrophe followed by vowel starts new syllable
                # e.g., "ba'i" should be "ba" + "'i", not "ba'" + "i"
                if post == "'" and len(text) > 1:
                    next_char = text[1]
                    # Check if next char is a vowel (i, u, e, o, etc.)
                    if next_char in ['i', 'u', 'e', 'o', 'a', 'A', 'I', 'U', 'E', 'O']:
                        return None, 0  # Don't treat as postscript
                
                return post, len(post)
        return None, 0
    
    def _could_be_multichar_consonant(self, text: str) -> bool:
        """Check if text starts with a multi-char consonant (3+ chars)"""
        for cons in self.alphabet.CONSONANTS.keys():
            if len(cons) > 2 and text.lower().startswith(cons):
                return True
        return False
    
    def _has_valid_root_ahead(self, text: str) -> bool:
        """Check if there's a valid root consonant ahead"""
        for root in self.alphabet.CONSONANTS.keys():
            if root != 'a' and text.lower().startswith(root):
                return True
        return False

