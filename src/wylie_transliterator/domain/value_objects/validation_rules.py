"""
Validation Rules Value Objects
Encapsulates EWTS validation rules as immutable value objects.
"""

from typing import Dict, Set, FrozenSet
from dataclasses import dataclass


@dataclass(frozen=True)
class SyllableStructureRules:
    """
    EWTS syllable structure rules.
    Based on THL Extended Wylie Transliteration Scheme.
    """
    
    # Valid prescripts and their allowed root consonants
    VALID_PRESCRIPT_COMBINATIONS: Dict[str, FrozenSet[str]] = None
    
    # Valid superscripts and their allowed root consonants  
    VALID_SUPERSCRIPT_COMBINATIONS: Dict[str, FrozenSet[str]] = None
    
    # Valid subscripts and their allowed root consonants
    VALID_SUBSCRIPT_COMBINATIONS: Dict[str, FrozenSet[str]] = None
    
    # Valid postscript consonants (suffix)
    VALID_POSTSCRIPTS: FrozenSet[str] = None
    
    # Valid second postscripts (post-suffix)
    VALID_SECOND_POSTSCRIPTS: FrozenSet[str] = None
    
    def __post_init__(self):
        """Initialize frozen sets for immutability"""
        if self.VALID_PRESCRIPT_COMBINATIONS is None:
            # Based on EWTS: g, d, b, m, 'a (apostrophe-a)
            object.__setattr__(self, 'VALID_PRESCRIPT_COMBINATIONS', {
                'g': frozenset(['n', 'ny', 's', 'sh', 'ts', 'y', 'z']),
                'd': frozenset(['k', 'g', 'ng', 'p', 'b', 'm', 'w', 'n', 'ny', 'r', 'l', 's', 'ts']),
                'b': frozenset(['k', 'g', 'c', 'j', 'ng', 's', 'sh', 'r', 'l', 'd', 'ts', 'w', 'z', 'zh', 'kss']),
                'm': frozenset(['kh', 'g', 'ng', 'ch', 'j', 'ny', 'th', 'd', 'n', 'dz', 'ts', 'tsh']),
                "'": frozenset(['a']),  # apostrophe as prescript for 'a
            })
        
        if self.VALID_SUPERSCRIPT_COMBINATIONS is None:
            # Based on EWTS: r, l, s
            object.__setattr__(self, 'VALID_SUPERSCRIPT_COMBINATIONS', {
                'r': frozenset(['k', 'g', 'ng', 'j', 'ny', 't', 'd', 'n', 'b', 'm', 'ts', 'dz']),
                'l': frozenset(['k', 'g', 'ng', 'c', 'j', 'p', 'b', 'h']),
                's': frozenset(['k', 'g', 'ng', 'ny', 't', 'd', 'n', 'p', 'b', 'm', 'ts']),
            })
        
        if self.VALID_SUBSCRIPT_COMBINATIONS is None:
            # Based on EWTS: r, l, y, w (and m for mantras)
            # Double subscripts: r+w, r+l
            object.__setattr__(self, 'VALID_SUBSCRIPT_COMBINATIONS', {
                'r': frozenset(['k', 'kh', 'g', 't', 'th', 'd', 'p', 'ph', 'b', 's', 'h', 
                               'tt', 'tth', 'dd', 'ddh']),  # Sanskrit included
                'l': frozenset(['k', 'g', 's', 'z', 'r']),
                'y': frozenset(['k', 'kh', 'g', 'p', 'ph', 'b', 'm', 's', 'h']),
                'w': frozenset(['k', 'kh', 'g', 't', 'th', 'd', 'ts', 'tsh', 'zh', 'z', 
                               's', 'r', 'l', 'sh', 'h']),
                'm': frozenset(['k', 'kh', 'g', 'ng', 'c', 'ch', 'j', 'ny', 't', 'th', 'd', 'n',
                               'p', 'ph', 'b', 'm', 'ts', 'tsh', 'dz', 'w', 'zh', 'z', 's', 'h',
                               'r', 'l', 'sh']),  # For mantras
                # Double subscripts
                'r+w': frozenset(['g', 'd']),  # grwa, drwa
                'r+l': frozenset(['k']),        # krla (rare)
            })
        
        if self.VALID_POSTSCRIPTS is None:
            # Valid suffix consonants
            object.__setattr__(self, 'VALID_POSTSCRIPTS', 
                             frozenset(['g', 'ng', 'd', 'n', 'b', 'm', 'r', 'l', 's']))
        
        if self.VALID_SECOND_POSTSCRIPTS is None:
            # Valid post-suffix consonants (only after specific suffixes)
            object.__setattr__(self, 'VALID_SECOND_POSTSCRIPTS',
                             frozenset(['s', 'd']))


@dataclass(frozen=True)
class ValidationErrorType:
    """Enumeration of validation error types"""
    UNKNOWN_CHARACTER: str = "unknown_character"
    INVALID_PRESCRIPT: str = "invalid_prescript"
    INVALID_SUPERSCRIPT: str = "invalid_superscript"
    INVALID_SUBSCRIPT: str = "invalid_subscript"
    INVALID_POSTSCRIPT: str = "invalid_postscript"
    INVALID_STACK: str = "invalid_stack"
    INVALID_VOWEL_COMBINATION: str = "invalid_vowel_combination"
    INVALID_SYLLABLE_STRUCTURE: str = "invalid_syllable_structure"
    MISSING_ROOT: str = "missing_root"
    AMBIGUOUS_PARSING: str = "ambiguous_parsing"


@dataclass(frozen=True)
class ValidationError:
    """Represents a single validation error"""
    error_type: str
    position: int
    syllable: str
    message: str
    suggestion: str = None
    
    def __str__(self) -> str:
        result = f"[{self.error_type}] at position {self.position}: {self.message}"
        if self.suggestion:
            result += f" (Suggestion: {self.suggestion})"
        return result


@dataclass(frozen=True)
class ValidationResult:
    """Result of validation with detailed error information"""
    is_valid: bool
    errors: tuple  # Tuple of ValidationError for immutability
    warnings: tuple = ()
    
    def __bool__(self) -> bool:
        return self.is_valid
    
    def get_error_summary(self) -> str:
        """Get human-readable summary of errors"""
        if self.is_valid:
            return "✓ Valid Extended Wylie"
        
        summary = [f"✗ Found {len(self.errors)} error(s):"]
        for error in self.errors:
            summary.append(f"  - {error}")
        
        if self.warnings:
            summary.append(f"\n⚠ {len(self.warnings)} warning(s):")
            for warning in self.warnings:
                summary.append(f"  - {warning}")
        
        return "\n".join(summary)


# Singleton instances
SYLLABLE_RULES = SyllableStructureRules()
ERROR_TYPES = ValidationErrorType()

