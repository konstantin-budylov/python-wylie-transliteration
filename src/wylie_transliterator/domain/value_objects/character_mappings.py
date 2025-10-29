"""
Character Mappings Value Objects
Immutable mappings between Wylie and Tibetan Unicode characters.
"""

from typing import Dict


class TibetanAlphabet:
    """
    Value Object containing Tibetan alphabet mappings.
    Based on THL Extended Wylie Transliteration Scheme (EWTS).
    """
    
    # Basic Tibetan consonants (30 letters)
    CONSONANTS: Dict[str, str] = {
        'k': '\u0F40',    # ཀ TIBETAN LETTER KA
        'kh': '\u0F41',   # ཁ TIBETAN LETTER KHA
        'g': '\u0F42',    # ག TIBETAN LETTER GA
        'gh': '\u0F43',   # གྷ TIBETAN LETTER GHA (Sanskrit)
        'ng': '\u0F44',   # ང TIBETAN LETTER NGA
        'c': '\u0F45',    # ཅ TIBETAN LETTER CA
        'ch': '\u0F46',   # ཆ TIBETAN LETTER CHA
        'j': '\u0F47',    # ཇ TIBETAN LETTER JA
        'ny': '\u0F49',   # ཉ TIBETAN LETTER NYA
        't': '\u0F4F',    # ཏ TIBETAN LETTER TA
        'th': '\u0F50',   # ཐ TIBETAN LETTER THA
        'd': '\u0F51',    # ད TIBETAN LETTER DA
        'dh': '\u0F52',   # དྷ TIBETAN LETTER DHA (Sanskrit)
        'n': '\u0F53',    # ན TIBETAN LETTER NA
        'p': '\u0F54',    # པ TIBETAN LETTER PA
        'ph': '\u0F55',   # ཕ TIBETAN LETTER PHA
        'b': '\u0F56',    # བ TIBETAN LETTER BA
        'bh': '\u0F57',   # བྷ TIBETAN LETTER BHA (Sanskrit)
        'm': '\u0F58',    # མ TIBETAN LETTER MA
        'ts': '\u0F59',   # ཙ TIBETAN LETTER TSA
        'tsh': '\u0F5A',  # ཚ TIBETAN LETTER TSHA
        'dz': '\u0F5B',   # ཛ TIBETAN LETTER DZA
        'dzh': '\u0F5C',  # ཛྷ TIBETAN LETTER DZHA (Sanskrit)
        'w': '\u0F5D',    # ཝ TIBETAN LETTER WA
        'zh': '\u0F5E',   # ཞ TIBETAN LETTER ZHA
        'z': '\u0F5F',    # ཟ TIBETAN LETTER ZA
        "'": '\u0F60',    # འ TIBETAN LETTER -A (a-chung)
        'y': '\u0F61',    # ཡ TIBETAN LETTER YA
        'r': '\u0F62',    # ར TIBETAN LETTER RA
        'l': '\u0F63',    # ལ TIBETAN LETTER LA
        'sh': '\u0F64',   # ཤ TIBETAN LETTER SHA
        'ss': '\u0F65',   # ཥ TIBETAN LETTER SSA (Sanskrit)
        's': '\u0F66',    # ས TIBETAN LETTER SA
        'h': '\u0F67',    # ཧ TIBETAN LETTER HA
        'a': '\u0F68',    # ཨ TIBETAN LETTER A
        # Sanskrit-specific (retroflex)
        'tt': '\u0F4A',   # ཊ TIBETAN LETTER TTA
        'tth': '\u0F4B',  # ཋ TIBETAN LETTER TTHA
        'dd': '\u0F4C',   # ཌ TIBETAN LETTER DDA
        'ddh': '\u0F4D',  # ཌྷ TIBETAN LETTER DDHA
        'nn': '\u0F4E',   # ཎ TIBETAN LETTER NNA
        'kss': '\u0F69',  # ཀྵ TIBETAN LETTER KSSA
        # Sanskrit retroflex capitals (for direct access in syllables)
        'Ta': '\u0F4A',   # ཊ TIBETAN LETTER TTA
        'Tha': '\u0F4B',  # ཋ TIBETAN LETTER TTHA
        'Da': '\u0F4C',   # ཌ TIBETAN LETTER DDA
        'Dha': '\u0F4D',  # ཌྷ TIBETAN LETTER DDHA
        'Na': '\u0F4E',   # ཎ TIBETAN LETTER NNA
        'Sha': '\u0F65',  # ཥ TIBETAN LETTER SSA
    }
    
    # Vowel signs
    VOWELS: Dict[str, str] = {
        'a': '',          # Inherent vowel (not written)
        'i': '\u0F72',    # ི TIBETAN VOWEL SIGN I
        'u': '\u0F74',    # ུ TIBETAN VOWEL SIGN U
        'e': '\u0F7A',    # ེ TIBETAN VOWEL SIGN E
        'o': '\u0F7C',    # ོ TIBETAN VOWEL SIGN O
        'A': '\u0F71',    # ཱ TIBETAN VOWEL SIGN AA (long a)
        'U': '\u0F71\u0F74',  # ཱུ Compound: long a + u (for mantras like hUM)
        '-i': '\u0F80',   # ྀ TIBETAN VOWEL SIGN REVERSED I
        '-I': '\u0F81',   # ཱྀ TIBETAN VOWEL SIGN REVERSED II
    }
    
    # Subscript consonants (for stacks)
    SUBSCRIPTS: Dict[str, str] = {
        'r': '\u0FB2',    # ྲ TIBETAN SUBJOINED LETTER RA
        'l': '\u0FB3',    # ླ TIBETAN SUBJOINED LETTER LA
        'y': '\u0FB1',    # ྱ TIBETAN SUBJOINED LETTER YA
        'w': '\u0FAD',    # ྭ TIBETAN SUBJOINED LETTER WA
        'v': '\u0FAD',    # ྭ Same as w (alternative notation)
        'm': '\u0FA8',    # ྨ TIBETAN SUBJOINED LETTER MA (for mantras)
    }
    
    # Subjoined forms (for use under superscripts)
    SUBJOINED: Dict[str, str] = {
        'k': '\u0F90',    # ྐ TIBETAN SUBJOINED LETTER KA
        'kh': '\u0F91',   # ྑ TIBETAN SUBJOINED LETTER KHA
        'g': '\u0F92',    # ྒ TIBETAN SUBJOINED LETTER GA
        'gh': '\u0F93',   # ྒྷ TIBETAN SUBJOINED LETTER GHA
        'ng': '\u0F94',   # ྔ TIBETAN SUBJOINED LETTER NGA
        'c': '\u0F95',    # ྕ TIBETAN SUBJOINED LETTER CA
        'ch': '\u0F96',   # ྖ TIBETAN SUBJOINED LETTER CHA
        'j': '\u0F97',    # ྗ TIBETAN SUBJOINED LETTER JA
        'ny': '\u0F99',   # ྙ TIBETAN SUBJOINED LETTER NYA
        't': '\u0F9F',    # ྟ TIBETAN SUBJOINED LETTER TA
        'th': '\u0FA0',   # ྠ TIBETAN SUBJOINED LETTER THA
        'd': '\u0FA1',    # ྡ TIBETAN SUBJOINED LETTER DA
        'dh': '\u0FA2',   # ྡྷ TIBETAN SUBJOINED LETTER DHA
        'n': '\u0FA3',    # ྣ TIBETAN SUBJOINED LETTER NA
        'p': '\u0FA4',    # ྤ TIBETAN SUBJOINED LETTER PA
        'ph': '\u0FA5',   # ྥ TIBETAN SUBJOINED LETTER PHA
        'b': '\u0FA6',    # ྦ TIBETAN SUBJOINED LETTER BA
        'bh': '\u0FA7',   # ྦྷ TIBETAN SUBJOINED LETTER BHA
        'm': '\u0FA8',    # ྨ TIBETAN SUBJOINED LETTER MA
        'ts': '\u0FA9',   # ྩ TIBETAN SUBJOINED LETTER TSA
        'tsh': '\u0FAA',  # ྪ TIBETAN SUBJOINED LETTER TSHA
        'dz': '\u0FAB',   # ྫ TIBETAN SUBJOINED LETTER DZA
        'dzh': '\u0FAC',  # ྫྷ TIBETAN SUBJOINED LETTER DZHA
        'w': '\u0FAD',    # ྭ TIBETAN SUBJOINED LETTER WA
        'zh': '\u0FAE',   # ྮ TIBETAN SUBJOINED LETTER ZHA
        'z': '\u0FAF',    # ྯ TIBETAN SUBJOINED LETTER ZA
        'y': '\u0FB1',    # ྱ TIBETAN SUBJOINED LETTER YA
        'r': '\u0FB2',    # ྲ TIBETAN SUBJOINED LETTER RA
        'l': '\u0FB3',    # ླ TIBETAN SUBJOINED LETTER LA
        'sh': '\u0FB4',   # ྴ TIBETAN SUBJOINED LETTER SHA
        'ss': '\u0FB5',   # ྵ TIBETAN SUBJOINED LETTER SSA
        's': '\u0FB6',    # ྶ TIBETAN SUBJOINED LETTER SA
        'h': '\u0FB7',    # ྷ TIBETAN SUBJOINED LETTER HA
        'tt': '\u0F9A',   # ྚ TIBETAN SUBJOINED LETTER TTA
        'tth': '\u0F9B',  # ྛ TIBETAN SUBJOINED LETTER TTHA
        'dd': '\u0F9C',   # ྜ TIBETAN SUBJOINED LETTER DDA
        'ddh': '\u0F9D',  # ྜྷ TIBETAN SUBJOINED LETTER DDHA
        'nn': '\u0F9E',   # ྞ TIBETAN SUBJOINED LETTER NNA
        'kss': '\u0FB9',  # ྐྵ TIBETAN SUBJOINED LETTER KSSA
    }
    
    # Punctuation marks
    PUNCTUATION: Dict[str, str] = {
        ' ': '\u0F0B',    # ་ TIBETAN MARK INTERSYLLABIC TSHEG
        '*': '\u0F0C',    # ༌ TIBETAN MARK DELIMITER TSHEG BSTAR
        '/': '\u0F0D',    # ། TIBETAN MARK SHAD
        '//': '\u0F0E',   # ༎ TIBETAN MARK NYIS SHAD
        ';': '\u0F0F',    # ༏ TIBETAN MARK TSHEG SHAD
        '|': '\u0F0D',    # ། TIBETAN MARK SHAD (alternative)
        '||': '\u0F0E',   # ༎ TIBETAN MARK NYIS SHAD (alternative)
        '!': '\u0F08',    # ༈ TIBETAN MARK SBRUL SHAD
        ':': '\u0F0E',    # ༎ Can represent double shad
        '_': '\u0F35',    # ༵ TIBETAN MARK NGAS BZUNG NYI ZLA
    }
    
    # Numerals
    NUMERALS: Dict[str, str] = {
        '0': '\u0F20',    # ༠ TIBETAN DIGIT ZERO
        '1': '\u0F21',    # ༡ TIBETAN DIGIT ONE
        '2': '\u0F22',    # ༢ TIBETAN DIGIT TWO
        '3': '\u0F23',    # ༣ TIBETAN DIGIT THREE
        '4': '\u0F24',    # ༤ TIBETAN DIGIT FOUR
        '5': '\u0F25',    # ༥ TIBETAN DIGIT FIVE
        '6': '\u0F26',    # ༦ TIBETAN DIGIT SIX
        '7': '\u0F27',    # ༧ TIBETAN DIGIT SEVEN
        '8': '\u0F28',    # ༨ TIBETAN DIGIT EIGHT
        '9': '\u0F29',    # ༩ TIBETAN DIGIT NINE
    }
    
    # Sanskrit marks
    SANSKRIT_MARKS: Dict[str, str] = {
        'M': '\u0F7E',    # ཾ TIBETAN SIGN RJES SU NGA RO (anusvara) - default
        'H': '\u0F7F',    # ཿ TIBETAN SIGN RNAM BCAD (visarga)
        '~M': '\u0F7E',   # Alternative notation
        '~H': '\u0F7F',   # Alternative notation
    }
    
    # Alternative anusvara for compound vowels (like hUM)
    ANUSVARA_AFTER_U: str = '\u0F83'  # ྃ TIBETAN SIGN SNA LDAN (after U/long vowels)
    
    # Sanskrit retroflex capitals
    SANSKRIT_RETROFLEX: Dict[str, str] = {
        'Ta': '\u0F4A',   # ཊ TIBETAN LETTER TTA
        'Tha': '\u0F4B',  # ཋ TIBETAN LETTER TTHA
        'Da': '\u0F4C',   # ཌ TIBETAN LETTER DDA
        'Dha': '\u0F4D',  # ཌྷ TIBETAN LETTER DDHA
        'Na': '\u0F4E',   # ཎ TIBETAN LETTER NNA
        'Sha': '\u0F65',  # ཥ TIBETAN LETTER SSA
    }


class SyllableRules:
    """
    Value Object containing the valid combinations for syllable components.
    """
    
    # Valid prescripts
    PRESCRIPTS = {'g', 'd', 'b', 'm', "'"}
    
    # Valid superscripts
    SUPERSCRIPTS = {'r', 'l', 's'}
    
    # Valid postscripts  
    POSTSCRIPTS = {'g', 'ng', 'd', 'n', 'b', 'm', 'r', 'l', 's', "'"}

