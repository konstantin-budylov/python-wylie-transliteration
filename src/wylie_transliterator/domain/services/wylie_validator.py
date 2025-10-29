"""
Wylie Validator Domain Service
Validates Extended Wylie input according to EWTS standard.
"""

from typing import List, Optional, Tuple
from ..value_objects.validation_rules import (
    ValidationResult, ValidationError, SYLLABLE_RULES, ERROR_TYPES
)
from ..value_objects.character_mappings import TibetanAlphabet
from ..models.syllable import SyllableComponents


class WylieValidator:
    """
    Domain Service for validating Extended Wylie transliteration input.
    
    Responsibilities:
    - Validate character existence in EWTS
    - Validate syllable structure rules
    - Validate consonant stack combinations
    - Provide detailed error messages
    
    Design Principles:
    - Single Responsibility: Only validation logic
    - Open/Closed: Extendable via rules without modification
    - Dependency Inversion: Depends on abstractions (value objects)
    """
    
    def __init__(self):
        self.alphabet = TibetanAlphabet()
        self.rules = SYLLABLE_RULES
        self._initialize_valid_characters()
    
    def _initialize_valid_characters(self):
        """Initialize set of all valid EWTS characters (DRY principle)"""
        self.valid_chars = set()
        
        # Add all known characters
        for mapping in [
            self.alphabet.CONSONANTS,
            self.alphabet.VOWELS,
            self.alphabet.SUBSCRIPTS,
            self.alphabet.PUNCTUATION,
            self.alphabet.SANSKRIT_MARKS,
            self.alphabet.NUMERALS,
            self.alphabet.SANSKRIT_RETROFLEX,
        ]:
            self.valid_chars.update(mapping.keys())
        
        # Add structural characters
        self.valid_chars.update([' ', '\n', '\t', '/', '|', '+', "'", '.', '-', '~'])
        
        # Add numbers
        self.valid_chars.update('0123456789')
        
        # Add capitals for Sanskrit
        self.valid_chars.update('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    
    def validate(self, wylie_text: str) -> ValidationResult:
        """
        Validate complete Wylie text.
        
        Returns ValidationResult with detailed error information.
        """
        errors: List[ValidationError] = []
        warnings: List[ValidationError] = []
        
        # Split into syllables for validation
        syllables = self._tokenize(wylie_text)
        
        position = 0
        for syllable_text in syllables:
            # Skip whitespace and punctuation-only tokens
            if self._is_punctuation_only(syllable_text):
                position += len(syllable_text)
                continue
            
            # Validate each syllable
            syllable_errors, syllable_warnings = self._validate_syllable(
                syllable_text, position
            )
            errors.extend(syllable_errors)
            warnings.extend(syllable_warnings)
            
            position += len(syllable_text)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
            warnings=tuple(warnings)
        )
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into syllables (KISS principle)"""
        tokens = []
        current = []
        
        for char in text:
            if char in [' ', '\t', '\n', '/', '|']:
                if current:
                    tokens.append(''.join(current))
                    current = []
                tokens.append(char)
            else:
                current.append(char)
        
        if current:
            tokens.append(''.join(current))
        
        return tokens
    
    def _is_punctuation_only(self, text: str) -> bool:
        """Check if text contains only punctuation/whitespace"""
        return all(c in [' ', '\t', '\n', '/', '|', '.'] for c in text)
    
    def _validate_syllable(
        self, syllable: str, position: int
    ) -> Tuple[List[ValidationError], List[ValidationError]]:
        """
        Validate a single syllable.
        
        Returns (errors, warnings)
        """
        errors = []
        warnings = []
        
        # 1. Check for unknown characters
        unknown = self._find_unknown_characters(syllable)
        if unknown:
            errors.append(ValidationError(
                error_type=ERROR_TYPES.UNKNOWN_CHARACTER,
                position=position,
                syllable=syllable,
                message=f"Unknown characters: {', '.join(unknown)}",
                suggestion="Check EWTS character list"
            ))
            return errors, warnings  # Stop further validation if unknown chars
        
        # 2. Check for special cases: numerals, standalone vowels, Sanskrit marks
        if self._is_numeral(syllable):
            return errors, warnings  # Numerals are always valid
        
        if self._is_standalone_vowel(syllable):
            return errors, warnings  # Standalone vowels are valid
        
        if self._is_sanskrit_mark_only(syllable):
            return errors, warnings  # Standalone Sanskrit marks are valid
        
        # 3. Try to parse syllable structure
        components = self._parse_syllable_structure(syllable)
        
        if components is None:
            errors.append(ValidationError(
                error_type=ERROR_TYPES.INVALID_SYLLABLE_STRUCTURE,
                position=position,
                syllable=syllable,
                message="Cannot parse syllable structure",
                suggestion="Check syllable component order"
            ))
            return errors, warnings
        
        # 4. Validate syllable components
        component_errors, component_warnings = self._validate_components(
            components, syllable, position
        )
        errors.extend(component_errors)
        warnings.extend(component_warnings)
        
        return errors, warnings
    
    def _is_numeral(self, syllable: str) -> bool:
        """Check if syllable is entirely numeric"""
        return all(c in '0123456789' for c in syllable)
    
    def _is_standalone_vowel(self, syllable: str) -> bool:
        """
        Check if syllable is a standalone vowel (with optional Sanskrit mark).
        Examples: oM, i, u, e, o, A, hUM (h+U+M is considered valid)
        """
        # Single vowel
        if syllable in self.alphabet.VOWELS:
            return True
        
        # Vowel + Sanskrit mark (e.g., oM)
        for vowel in sorted(self.alphabet.VOWELS.keys(), key=len, reverse=True):
            if syllable.startswith(vowel):
                remainder = syllable[len(vowel):]
                if remainder in self.alphabet.SANSKRIT_MARKS or remainder == '':
                    return True
        
        # Special case: consonant + vowel + Sanskrit mark (like hUM)
        # This is handled by normal syllable parsing, so return False here
        return False
    
    def _is_sanskrit_mark_only(self, syllable: str) -> bool:
        """Check if syllable is only Sanskrit marks"""
        return syllable in self.alphabet.SANSKRIT_MARKS
    
    def _find_unknown_characters(self, syllable: str) -> List[str]:
        """Find characters not in EWTS (DRY principle)"""
        unknown = []
        i = 0
        
        while i < len(syllable):
            # Try multi-char sequences first
            found = False
            for length in [3, 2, 1]:
                if i + length <= len(syllable):
                    substr = syllable[i:i+length]
                    if substr in self.valid_chars:
                        i += length
                        found = True
                        break
            
            if not found:
                if syllable[i] not in self.valid_chars:
                    unknown.append(syllable[i])
                i += 1
        
        return unknown
    
    def _parse_syllable_structure(self, syllable: str) -> Optional[SyllableComponents]:
        """
        Parse syllable into components for validation.
        Uses multi-strategy approach to find best VALID parse.
        Prioritizes valid parses (0 errors) over longer parses.
        Returns None if parsing fails.
        """
        # Try different parsing strategies
        strategies = [
            self._parse_simple,           # root + modifiers
            self._parse_with_subscript,   # root + subscript + modifiers
            self._parse_with_superscript, # superscript + root + modifiers
            self._parse_with_prescript,   # prescript + root + modifiers
            self._parse_full,             # prescript + superscript + root + subscript + modifiers
        ]
        
        valid_parses = []  # Parses with 0 errors
        invalid_parses = []  # Parses with errors
        
        for strategy in strategies:
            components, length = strategy(syllable)
            if components and length > 0:
                # Check validity of this parse
                errors, warnings = self._validate_components(components, syllable, 0)
                
                if len(errors) == 0:
                    valid_parses.append((components, length, errors, warnings))
                else:
                    invalid_parses.append((components, length, errors, warnings))
        
        # Filter parses that consume the entire syllable (or close to it)
        syllable_len = len(syllable)
        
        # A valid parse should consume the entire syllable
        # (Allow syllable_len or syllable_len-1 for implicit 'a' vowel)
        complete_valid_parses = [p for p in valid_parses if p[1] >= syllable_len - 1]
        complete_invalid_parses = [p for p in invalid_parses if p[1] >= syllable_len - 1]
        
        # Prefer complete valid parses
        if complete_valid_parses:
            # Among complete valid parses, pick the longest
            best = max(complete_valid_parses, key=lambda x: x[1])
            return best[0]
        elif complete_invalid_parses:
            # If no complete valid parse, pick complete invalid with fewest errors
            best = min(complete_invalid_parses, key=lambda x: (len(x[2]), -x[1]))
            return best[0]
        elif valid_parses:
            # Fall back to any valid parse (even incomplete)
            best = max(valid_parses, key=lambda x: x[1])
            return best[0]
        elif invalid_parses:
            # Last resort: incomplete invalid parse
            best = min(invalid_parses, key=lambda x: (len(x[2]), -x[1]))
            return best[0]
        
        return None
    
    def _parse_simple(self, syllable: str) -> Tuple[Optional[SyllableComponents], int]:
        """Parse: root [+vowel] [+postscript]"""
        pos = 0
        
        # Match root
        root = None
        for cons in sorted(self.alphabet.CONSONANTS.keys(), key=len, reverse=True):
            if syllable[pos:].startswith(cons) or syllable[pos:].lower().startswith(cons):
                root = syllable[pos:pos+len(cons)] if syllable[pos:].startswith(cons) else cons
                pos += len(cons)
                break
        
        if not root:
            return None, 0
        
        # Match vowel (including explicit 'a' when not implicit)
        vowel = None
        for v in sorted(self.alphabet.VOWELS.keys(), key=len, reverse=True):
            if syllable[pos:].startswith(v):
                # Match 'a' only if there's more content after (explicit 'a')
                if v == 'a' and pos + 1 < len(syllable):
                    vowel = v
                    pos += len(v)
                    break
                elif v != 'a':
                    vowel = v
                    pos += len(v)
                    break
        
        # Match postscript
        postscript1 = None
        for post in sorted(self.rules.VALID_POSTSCRIPTS, key=len, reverse=True):
            if syllable[pos:].lower().startswith(post):
                postscript1 = post
                pos += len(post)
                break
        
        # Match second postscript
        postscript2 = None
        if postscript1:
            for post2 in sorted(self.rules.VALID_SECOND_POSTSCRIPTS, key=len, reverse=True):
                if syllable[pos:].lower().startswith(post2):
                    postscript2 = post2
                    pos += len(post2)
                    break
        
        return SyllableComponents(
            root=root.lower() if root else None,
            vowel=vowel,
            postscript1=postscript1,
            postscript2=postscript2
        ), pos
    
    def _parse_with_subscript(self, syllable: str) -> Tuple[Optional[SyllableComponents], int]:
        """Parse: root + subscript [+vowel] [+postscript]"""
        pos = 0
        
        # Match root
        root = None
        for cons in sorted(self.alphabet.CONSONANTS.keys(), key=len, reverse=True):
            if syllable[pos:].startswith(cons) or syllable[pos:].lower().startswith(cons):
                root = syllable[pos:pos+len(cons)] if syllable[pos:].startswith(cons) else cons
                pos += len(cons)
                break
        
        if not root:
            return None, 0
        
        # Match subscript (can be double like 'r+w')
        subscripts_matched = []
        for sub in sorted(self.alphabet.SUBSCRIPTS.keys(), key=len, reverse=True):
            if syllable[pos:].lower().startswith(sub):
                subscripts_matched.append(sub)
                pos += len(sub)
                
                # Try to match second subscript
                for sub2 in sorted(self.alphabet.SUBSCRIPTS.keys(), key=len, reverse=True):
                    if syllable[pos:].lower().startswith(sub2):
                        subscripts_matched.append(sub2)
                        pos += len(sub2)
                        break
                break
        
        if not subscripts_matched:
            return None, 0  # This strategy requires subscript
        
        subscript = '+'.join(subscripts_matched) if len(subscripts_matched) > 1 else subscripts_matched[0]
        
        # Match vowel (including explicit 'a' when not implicit)
        vowel = None
        for v in sorted(self.alphabet.VOWELS.keys(), key=len, reverse=True):
            if syllable[pos:].startswith(v):
                # Match 'a' only if there's more content after (explicit 'a')
                if v == 'a' and pos + 1 < len(syllable):
                    vowel = v
                    pos += len(v)
                    break
                elif v != 'a':
                    vowel = v
                    pos += len(v)
                    break
        
        # Match postscript
        postscript1 = None
        for post in sorted(self.rules.VALID_POSTSCRIPTS, key=len, reverse=True):
            if syllable[pos:].lower().startswith(post):
                postscript1 = post
                pos += len(post)
                break
        
        postscript2 = None
        if postscript1:
            for post2 in sorted(self.rules.VALID_SECOND_POSTSCRIPTS, key=len, reverse=True):
                if syllable[pos:].lower().startswith(post2):
                    postscript2 = post2
                    pos += len(post2)
                    break
        
        return SyllableComponents(
            root=root.lower() if root else None,
            subscript=subscript,
            vowel=vowel,
            postscript1=postscript1,
            postscript2=postscript2
        ), pos
    
    def _parse_with_superscript(self, syllable: str) -> Tuple[Optional[SyllableComponents], int]:
        """Parse: superscript + root [+vowel] [+postscript]"""
        pos = 0
        
        # Match superscript
        superscript = None
        for sup in sorted(self.rules.VALID_SUPERSCRIPT_COMBINATIONS.keys(),
                         key=len, reverse=True):
            if syllable[pos:].lower().startswith(sup):
                superscript = sup
                pos += len(sup)
                break
        
        if not superscript:
            return None, 0
        
        # Match root
        root = None
        for cons in sorted(self.alphabet.CONSONANTS.keys(), key=len, reverse=True):
            if syllable[pos:].startswith(cons) or syllable[pos:].lower().startswith(cons):
                root = syllable[pos:pos+len(cons)] if syllable[pos:].startswith(cons) else cons
                pos += len(cons)
                break
        
        if not root:
            return None, 0
        
        # Match vowel and postscripts (same as simple)
        vowel = None
        for v in sorted([k for k in self.alphabet.VOWELS.keys() if k != 'a'], 
                       key=len, reverse=True):
            if syllable[pos:].startswith(v):
                vowel = v
                pos += len(v)
                break
        
        postscript1 = None
        for post in sorted(self.rules.VALID_POSTSCRIPTS, key=len, reverse=True):
            if syllable[pos:].lower().startswith(post):
                postscript1 = post
                pos += len(post)
                break
        
        postscript2 = None
        if postscript1:
            for post2 in sorted(self.rules.VALID_SECOND_POSTSCRIPTS, key=len, reverse=True):
                if syllable[pos:].lower().startswith(post2):
                    postscript2 = post2
                    pos += len(post2)
                    break
        
        return SyllableComponents(
            superscript=superscript,
            root=root.lower() if root else None,
            vowel=vowel,
            postscript1=postscript1,
            postscript2=postscript2
        ), pos
    
    def _parse_with_prescript(self, syllable: str) -> Tuple[Optional[SyllableComponents], int]:
        """Parse: prescript + root [+vowel] [+postscript]"""
        pos = 0
        
        # Match prescript
        prescript = None
        for pre in sorted(self.rules.VALID_PRESCRIPT_COMBINATIONS.keys(), 
                         key=len, reverse=True):
            if syllable[pos:].lower().startswith(pre):
                prescript = pre
                pos += len(pre)
                break
        
        if not prescript:
            return None, 0
        
        # Match root
        root = None
        for cons in sorted(self.alphabet.CONSONANTS.keys(), key=len, reverse=True):
            if syllable[pos:].startswith(cons) or syllable[pos:].lower().startswith(cons):
                root = syllable[pos:pos+len(cons)] if syllable[pos:].startswith(cons) else cons
                pos += len(cons)
                break
        
        if not root:
            return None, 0
        
        # Match vowel and postscripts
        vowel = None
        for v in sorted([k for k in self.alphabet.VOWELS.keys() if k != 'a'], 
                       key=len, reverse=True):
            if syllable[pos:].startswith(v):
                vowel = v
                pos += len(v)
                break
        
        postscript1 = None
        for post in sorted(self.rules.VALID_POSTSCRIPTS, key=len, reverse=True):
            if syllable[pos:].lower().startswith(post):
                postscript1 = post
                pos += len(post)
                break
        
        postscript2 = None
        if postscript1:
            for post2 in sorted(self.rules.VALID_SECOND_POSTSCRIPTS, key=len, reverse=True):
                if syllable[pos:].lower().startswith(post2):
                    postscript2 = post2
                    pos += len(post2)
                    break
        
        return SyllableComponents(
            prescript=prescript,
            root=root.lower() if root else None,
            vowel=vowel,
            postscript1=postscript1,
            postscript2=postscript2
        ), pos
    
    def _parse_full(self, syllable: str) -> Tuple[Optional[SyllableComponents], int]:
        """Parse: [prescript] + [superscript] + root + [subscript] + [vowel] + [postscript]"""
        pos = 0
        
        # Match prescript
        prescript = None
        for pre in sorted(self.rules.VALID_PRESCRIPT_COMBINATIONS.keys(), 
                         key=len, reverse=True):
            if syllable[pos:].lower().startswith(pre):
                prescript = pre
                pos += len(pre)
                break
        
        # Match superscript
        superscript = None
        for sup in sorted(self.rules.VALID_SUPERSCRIPT_COMBINATIONS.keys(),
                         key=len, reverse=True):
            if syllable[pos:].lower().startswith(sup):
                superscript = sup
                pos += len(sup)
                break
        
        # Match root (required)
        root = None
        for cons in sorted(self.alphabet.CONSONANTS.keys(), key=len, reverse=True):
            if syllable[pos:].startswith(cons) or syllable[pos:].lower().startswith(cons):
                root = syllable[pos:pos+len(cons)] if syllable[pos:].startswith(cons) else cons
                pos += len(cons)
                break
        
        if not root:
            return None, 0
        
        # Match subscript
        subscript = None
        for sub in sorted(self.alphabet.SUBSCRIPTS.keys(), key=len, reverse=True):
            if syllable[pos:].lower().startswith(sub):
                subscript = sub
                pos += len(sub)
                break
        
        # Match vowel (including explicit 'a' when not implicit)
        vowel = None
        for v in sorted(self.alphabet.VOWELS.keys(), key=len, reverse=True):
            if syllable[pos:].startswith(v):
                # Match 'a' only if there's more content after (explicit 'a')
                if v == 'a' and pos + 1 < len(syllable):
                    vowel = v
                    pos += len(v)
                    break
                elif v != 'a':
                    vowel = v
                    pos += len(v)
                    break
        
        # Match postscripts
        postscript1 = None
        for post in sorted(self.rules.VALID_POSTSCRIPTS, key=len, reverse=True):
            if syllable[pos:].lower().startswith(post):
                postscript1 = post
                pos += len(post)
                break
        
        postscript2 = None
        if postscript1:
            for post2 in sorted(self.rules.VALID_SECOND_POSTSCRIPTS, key=len, reverse=True):
                if syllable[pos:].lower().startswith(post2):
                    postscript2 = post2
                    pos += len(post2)
                    break
        
        # Only return if we have prescript OR superscript (otherwise it's redundant with simpler strategies)
        if not prescript and not superscript:
            return None, 0
        
        return SyllableComponents(
            prescript=prescript,
            superscript=superscript,
            root=root.lower() if root else None,
            subscript=subscript,
            vowel=vowel,
            postscript1=postscript1,
            postscript2=postscript2
        ), pos
    
    def _validate_components(
        self, 
        components: SyllableComponents,
        syllable: str,
        position: int
    ) -> Tuple[List[ValidationError], List[ValidationError]]:
        """Validate syllable components according to EWTS rules"""
        errors = []
        warnings = []
        
        # Validate prescript + root combination
        if components.prescript and components.root:
            valid_roots = self.rules.VALID_PRESCRIPT_COMBINATIONS.get(
                components.prescript, frozenset()
            )
            if components.root not in valid_roots:
                errors.append(ValidationError(
                    error_type=ERROR_TYPES.INVALID_PRESCRIPT,
                    position=position,
                    syllable=syllable,
                    message=f"Invalid prescript '{components.prescript}' "
                           f"before root '{components.root}'",
                    suggestion=f"Valid roots after '{components.prescript}': "
                              f"{', '.join(sorted(valid_roots))}"
                ))
        
        # Validate superscript + root combination
        if components.superscript and components.root:
            valid_roots = self.rules.VALID_SUPERSCRIPT_COMBINATIONS.get(
                components.superscript, frozenset()
            )
            if components.root not in valid_roots:
                errors.append(ValidationError(
                    error_type=ERROR_TYPES.INVALID_SUPERSCRIPT,
                    position=position,
                    syllable=syllable,
                    message=f"Invalid superscript '{components.superscript}' "
                           f"above root '{components.root}'",
                    suggestion=f"Valid roots under '{components.superscript}': "
                              f"{', '.join(sorted(valid_roots))}"
                ))
        
        # Validate subscript + root combination
        if components.subscript and components.root:
            # Check if it's a valid single or double subscript
            valid_roots = self.rules.VALID_SUBSCRIPT_COMBINATIONS.get(
                components.subscript, frozenset()
            )
            if valid_roots and components.root not in valid_roots:
                errors.append(ValidationError(
                    error_type=ERROR_TYPES.INVALID_SUBSCRIPT,
                    position=position,
                    syllable=syllable,
                    message=f"Invalid subscript '{components.subscript}' "
                           f"below root '{components.root}'",
                    suggestion=f"Valid roots above '{components.subscript}': "
                              f"{', '.join(sorted(valid_roots))}"
                ))
            elif not valid_roots:
                # Unknown subscript combination - might be double subscript without validation rules
                # Allow it as a warning rather than error
                warnings.append(ValidationError(
                    error_type=ERROR_TYPES.AMBIGUOUS_PARSING,
                    position=position,
                    syllable=syllable,
                    message=f"Unusual subscript combination '{components.subscript}' "
                           f"with root '{components.root}'",
                    suggestion="Verify this is correct EWTS"
                ))
        
        # Validate postscript
        if components.postscript1:
            if components.postscript1 not in self.rules.VALID_POSTSCRIPTS:
                errors.append(ValidationError(
                    error_type=ERROR_TYPES.INVALID_POSTSCRIPT,
                    position=position,
                    syllable=syllable,
                    message=f"Invalid postscript '{components.postscript1}'",
                    suggestion=f"Valid postscripts: "
                              f"{', '.join(sorted(self.rules.VALID_POSTSCRIPTS))}"
                ))
        
        # Validate second postscript
        if components.postscript2:
            if components.postscript2 not in self.rules.VALID_SECOND_POSTSCRIPTS:
                errors.append(ValidationError(
                    error_type=ERROR_TYPES.INVALID_POSTSCRIPT,
                    position=position,
                    syllable=syllable,
                    message=f"Invalid second postscript '{components.postscript2}'",
                    suggestion=f"Valid second postscripts: "
                              f"{', '.join(sorted(self.rules.VALID_SECOND_POSTSCRIPTS))}"
                ))
        
        return errors, warnings

