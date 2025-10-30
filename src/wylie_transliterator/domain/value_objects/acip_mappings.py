"""
ACIP Character Mappings Value Objects
Immutable mappings for ACIP (Asian Classics Input Project) transliteration.

Reference: http://www.asianclassics.org/download/tibetancode/ticode.pdf
"""

import re
from typing import Dict, Pattern, List


class ACIPAlphabet:
    """
    Value Object containing ACIP alphabet mappings.
    
    ACIP (Asian Classics Input Project) is a widely-used Tibetan input system
    for digitizing Buddhist texts. This class provides bidirectional mappings
    between ACIP and EWTS (Extended Wylie).
    
    Key Differences from EWTS:
    - ACIP uses uppercase for consonants (K, KH, G, etc.)
    - TS in ACIP = tsh in EWTS
    - TZ in ACIP = ts in EWTS
    - i in ACIP = -I in EWTS (reverse vowel)
    - EE in ACIP = ai in EWTS
    - OO in ACIP = au in EWTS
    """
    
    # Basic ACIP to EWTS consonant mappings
    CONSONANTS_ACIP_TO_EWTS: Dict[str, str] = {
        # Basic Tibetan consonants (ACIP uses uppercase)
        'K': 'k',
        'KH': 'kh',
        'G': 'g',
        'NG': 'ng',
        'C': 'c',
        'CH': 'ch',
        'J': 'j',
        'NY': 'ny',
        'T': 't',
        'TH': 'th',
        'D': 'd',
        'N': 'n',
        'P': 'p',
        'PH': 'ph',
        'B': 'b',
        'M': 'm',
        'TS': 'tsh',    # Important: ACIP TS = EWTS tsh
        'TSH': 'tsh',   # Alternative
        'TZ': 'ts',     # Important: ACIP TZ = EWTS ts
        'DZ': 'dz',
        'W': 'w',
        'V': 'w',       # ACIP V = EWTS w
        'ZH': 'zh',
        'Z': 'z',
        "'": "'",
        'Y': 'y',
        'R': 'r',
        'L': 'l',
        'SH': 'sh',     # ACIP uppercase SH = EWTS lowercase sh
        'S': 's',
        'H': 'h',
    }
    
    # Special ACIP patterns for sh (lowercase in ACIP = Sh in EWTS)
    # In ACIP: 'sh' (lowercase) = Sanskrit retroflex Sh in EWTS
    # In ACIP: 'SH' (uppercase) = regular sh in EWTS
    SPECIAL_SH_MAPPING = {
        'sh': 'Sh',     # ACIP lowercase sh = EWTS Sh (Sanskrit)
        'SH': 'sh',     # ACIP uppercase SH = EWTS sh (regular)
    }
    
    # ACIP vowel mappings (different from EWTS)
    VOWELS_ACIP_TO_EWTS: Dict[str, str] = {
        'A': 'a',
        'I': 'i',       # ACIP I = EWTS i
        'U': 'u',
        'E': 'e',
        'O': 'o',
        'EE': 'ai',     # ACIP EE = EWTS ai
        'OO': 'au',     # ACIP OO = EWTS au
        'i': '-I',      # ACIP i (lowercase) = EWTS -I (reverse vowel)
        "'i": '-i',     # ACIP 'i = EWTS -i
    }
    
    # ACIP punctuation to EWTS
    PUNCTUATION_ACIP_TO_EWTS: Dict[str, str] = {
        ';': '|',       # ACIP ; = EWTS |
        ',': '/',       # ACIP , = EWTS /
        '`': '!',       # ACIP ` = EWTS !
        '\\': '?',      # ACIP \ = EWTS ?
        ':': 'H',       # ACIP : = EWTS H (visarga)
        '%': '~X',      # ACIP % = EWTS ~X
    }
    
    # Reverse mappings (EWTS to ACIP)
    CONSONANTS_EWTS_TO_ACIP: Dict[str, str] = {
        'k': 'K',
        'kh': 'KH',
        'g': 'G',
        'ng': 'NG',
        'c': 'C',
        'ch': 'CH',
        'j': 'J',
        'ny': 'NY',
        't': 'T',
        'th': 'TH',
        'd': 'D',
        'n': 'N',
        'p': 'P',
        'ph': 'PH',
        'b': 'B',
        'm': 'M',
        'tsh': 'TS',    # EWTS tsh = ACIP TS
        'ts': 'TZ',     # EWTS ts = ACIP TZ
        'dz': 'DZ',
        'w': 'W',
        'zh': 'ZH',
        'z': 'Z',
        "'": "'",
        'y': 'Y',
        'r': 'R',
        'l': 'L',
        'sh': 'SH',
        'Sh': 'sh',     # EWTS Sh = ACIP sh (lowercase)
        's': 'S',
        'h': 'H',
    }
    
    VOWELS_EWTS_TO_ACIP: Dict[str, str] = {
        'a': 'A',
        'i': 'I',
        'u': 'U',
        'e': 'E',
        'o': 'O',
        'ai': 'EE',
        'au': 'OO',
        '-I': 'i',      # EWTS -I = ACIP i
        '-i': "'i",     # EWTS -i = ACIP 'i
    }
    
    PUNCTUATION_EWTS_TO_ACIP: Dict[str, str] = {
        '|': ';',
        '/': ',',
        '!': '`',
        '?': '\\',
        'H': ':',
        '~X': '%',
    }


class ACIPPatterns:
    """
    Regular expression patterns for ACIP conversion.
    """
    
    # Comments in ACIP
    COMMENT_AT: Pattern = re.compile(r'@[^ ]* *')
    COMMENT_BRACKET: Pattern = re.compile(r'\[[^\]]*\]')
    
    # Parentheses: /.../ in ACIP = (...) in EWTS
    PARENS: Pattern = re.compile(r'\/([^/]*)(\/)' )
    
    # Asterisks encoding (special handling)
    ASTERISK_ENCODING: Pattern = re.compile(r'\*+')
    
    # Vowel after consonant patterns
    # B'I in ACIP = bi in EWTS
    VOWEL_AFTER_CONS: Pattern = re.compile(
        r"([BCDGHJKLMNPRSTWYZ])'([AEOUI])"
    )
    
    # Stacked consonants pattern
    CONSONANT_STACK: Pattern = re.compile(
        r'([BCDGHJKLMNPRSTWYZ]+)([aeiouAEIOU])'
    )
    
    # GA-YAS pattern (GA-YAS = g.yas in EWTS)
    GA_YAS_PATTERN: Pattern = re.compile(
        r'([BCDGHJKLMN\'PRSTWYZhdtn])A-'
    )
    
    # Space normalization patterns
    SPACE_BEFORE_PUNCT: Pattern = re.compile(
        r'([aeiouIAEU]g|[gk][aeiouAEIU]|[;!/|]) +([;!/|])'
    )
    SPACE_AFTER_PUNCT: Pattern = re.compile(
        r'([;!/|H]) +'
    )


class ACIPStandardStacks:
    """
    Standard Tibetan consonant stacks that don't need + signs.
    
    These are common valid stacks in Tibetan orthography.
    When converting from ACIP, we need to identify these to know
    when NOT to insert + signs between consonants.
    
    Based on pyewts STD_TIB_PATTERN which allows [rwy]* subscripts after base stacks.
    """
    
    # Compile pattern to match valid Tibetan stacks (matching pyewts)
    # Base stacks + optional subscripts [rwy]*
    STD_TIB_PATTERN: Pattern = re.compile(
        r"^([bcdgjklm'npstzhSDTN]|bgl|dm|sm|sn|kl|dk|bk|bkl|rk|lk|sk|brk|bsk|kh|mkh|'kh|"
        r"gl|dg|bg|mg|'g|rg|lg|sg|brg|bsg|ng|dng|mng|rng|lng|sng|brng|bsng|gc|bc|lc|"
        r"ch|mch|'ch|mj|'j|rj|lj|brj|ny|gny|mny|rny|sny|brny|bsny|gt|bt|rt|lt|st|brt|"
        r"blt|bst|th|mth|'th|gd|bd|md|'d|rd|ld|sd|brd|bld|bsd|gn|mn|rn|brn|bsn|dp|lp|"
        r"sp|ph|'ph|bl|db|'b|rb|lb|sb|rm|ts|gts|bts|rts|sts|brts|bsts|tsh|mtsh|'tsh|"
        r"dz|mdz|'dz|rdz|brdz|zh|gzh|bzh|zl|gz|bz|bzl|rl|brl|sh|gsh|bsh|sl|gs|bs|bsl|lh)"
        r"[rwy]*$",
        re.IGNORECASE
    )
    
    # List of prefix stacks (for add_plus logic)
    STD_TIB_STACKS_PREFIX = [
        "bg", "dm", "dk", "bk", "brk", "bsk", "mkh", "'kh", "dg", "bg", "mg", "'g",
        "brg", "bsg", "dng", "mng", "brng", "bsng", "gc", "bc", "ch", "mch", "'ch",
        "mj", "'j", "brj", "gny", "mny", "brny", "bsny", "gt", "bt", "brt", "blt",
        "bst", "mth", "'th", "gd", "bd", "md", "'d", "brd", "bld", "bsd", "gn", "mn",
        "brn", "bsn", "dp", "ph", "'ph", "bl", "db", "'b", "gts", "bts", "brts",
        "bsts", "tsh", "mtsh", "'tsh", "mdz", "'dz", "brdz", "gzh", "bzh", "gz",
        "bz", "bzl", "brl", "gsh", "bsh", "gs", "bs", "bsl"
    ]
    
    # Patterns that need special subscript handling
    SUBSCRIPTS = ['r', 'l', 'y', 'w']
    
    @classmethod
    def is_valid_stack(cls, consonants: str) -> bool:
        """Check if consonant combination is a valid Tibetan stack using regex pattern."""
        return cls.STD_TIB_PATTERN.match(consonants.lower()) is not None
    
    @classmethod
    def needs_plus(cls, consonants: str) -> bool:
        """Check if consonants need + between them (Sanskrit, etc.)."""
        return not cls.is_valid_stack(consonants)

