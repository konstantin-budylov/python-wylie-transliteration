"""
Comparison tests: python-wylie-transliteration vs pyewts (Basic Features)

Tests basic Wylie transliteration to ensure compatibility with pyewts.
"""

import unittest
import sys
import os

# Add pyewts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../pyewts'))

try:
    import pyewts
    PYEWTS_AVAILABLE = True
except ImportError:
    PYEWTS_AVAILABLE = False

from wylie_transliterator import TransliterationService


@unittest.skipUnless(PYEWTS_AVAILABLE, "pyewts not available for comparison")
class TestPyewtsComparisonBasic(unittest.TestCase):
    """Compare basic transliteration features with pyewts"""
    
    def setUp(self):
        self.pyewts = pyewts.pyewts()
        self.service = TransliterationService()
    
    def _compare(self, wylie_input, preserve_spaces=False):
        """Helper to compare outputs"""
        expected = self.pyewts.toUnicode(wylie_input)
        result = self.service.transliterate_wylie_to_tibetan(wylie_input, preserve_spaces=preserve_spaces)
        self.assertEqual(result, expected, 
                        f"\nInput: {wylie_input}\nExpected: {expected}\nGot: {result}")
    
    # === BASIC CONSONANTS ===
    
    def test_basic_consonants(self):
        """Test all basic Tibetan consonants"""
        consonants = ['ka', 'kha', 'ga', 'nga', 'ca', 'cha', 'ja', 'nya',
                     'ta', 'tha', 'da', 'na', 'pa', 'pha', 'ba', 'ma',
                     'tsa', 'tsha', 'dza', 'wa', 'zha', 'za', 'ya', 'ra',
                     'la', 'sha', 'sa', 'ha', 'a']
        
        for cons in consonants:
            with self.subTest(consonant=cons):
                self._compare(cons)
    
    def test_consonants_with_vowels(self):
        """Test consonants with all vowels"""
        test_cases = [
            'ka', 'ki', 'ku', 'ke', 'ko',
            'pa', 'pi', 'pu', 'pe', 'po',
        ]
        
        for wylie in test_cases:
            with self.subTest(wylie=wylie):
                self._compare(wylie)
    
    def test_diphthongs(self):
        """Test diphthongs ai and au"""
        test_cases = [
            'kai',  # ཀཻ
            'kau',  # ཀཽ
            'pai',  # པཻ
            'pau',  # པཽ
        ]
        
        for wylie in test_cases:
            with self.subTest(wylie=wylie):
                self._compare(wylie)
    
    # === COMPLEX STACKS ===
    
    def test_subscripts(self):
        """Test consonants with subscripts"""
        test_cases = [
            'kya', 'kra', 'kla', 'kwa',
            'pya', 'pra', 'pla', 'pwa',
            'bya', 'bra', 'bla', 'bwa',
        ]
        
        for wylie in test_cases:
            with self.subTest(wylie=wylie):
                self._compare(wylie)
    
    def test_superscripts(self):
        """Test consonants with superscripts"""
        test_cases = [
            'rka', 'rga', 'rnga', 'rja', 'rnya',
            'rta', 'rda', 'rna', 'rba', 'rma',
            'rtsa', 'rdza',
            'lka', 'lga', 'lnga', 'lca', 'lja',
            'lta', 'lda', 'lpa', 'lba',
            'ska', 'sga', 'snga', 'snya', 'sta',
            'sda', 'sna', 'spa', 'sba', 'sma',
            'stsa',
        ]
        
        for wylie in test_cases:
            with self.subTest(wylie=wylie):
                self._compare(wylie)
    
    def test_prescripts(self):
        """Test consonants with prescripts"""
        test_cases = [
            'gya', 'gra', 'gla', 'gwa',
            'dwa', 'dra',
            'bya', 'bra', 'bla', 'bwa',
            'mya', 'mra',
        ]
        
        for wylie in test_cases:
            with self.subTest(wylie=wylie):
                self._compare(wylie)
    
    def test_complex_stacks(self):
        """Test complex consonant stacks"""
        test_cases = [
            'bsgrubs',  # བསྒྲུབས
            'bkra',     # བཀྲ
            'dkon',     # དཀོན
            'bskyabs',  # བསྐྱབས
            'sgra',     # སྒྲ
            'spyan',    # སྤྱན
        ]
        
        for wylie in test_cases:
            with self.subTest(wylie=wylie):
                self._compare(wylie)
    
    # === POSTSCRIPTS ===
    
    def test_single_postscripts(self):
        """Test single final consonants"""
        test_cases = [
            'kag', 'kang', 'kad', 'kan', 'kab', 'kam', 'kar', 'kal', 'kas',
        ]
        
        for wylie in test_cases:
            with self.subTest(wylie=wylie):
                self._compare(wylie)
    
    def test_double_postscripts(self):
        """Test double final consonants"""
        test_cases = [
            'gangs',  # ག + ང + ས
            'drangs', # དྲ + ང + ས
            'bangs',  # བ + ང + ས
        ]
        
        for wylie in test_cases:
            with self.subTest(wylie=wylie):
                self._compare(wylie)
    
    # === GENITIVE PARTICLES ===
    
    def test_genitive_particles(self):
        """Test genitive particles with apostrophe"""
        test_cases = [
            "ba'i",    # བའི
            "ka'i",    # ཀའི
            "nga'i",   # ངའི
            "pa'o",    # པའོ
            "ma'am",   # མའམ
            "da'ang",  # དའང
        ]
        
        for wylie in test_cases:
            with self.subTest(wylie=wylie):
                self._compare(wylie)
    
    # === VOWEL-INITIAL SYLLABLES ===
    
    def test_vowel_initial(self):
        """Test syllables starting with vowels"""
        test_cases = [
            'a',   # ཨ
            'i',   # ཨི
            'u',   # ཨུ
            'e',   # ཨེ
            'o',   # ཨོ
            'om',  # ཨོམ
            'ang', # ཨང
        ]
        
        for wylie in test_cases:
            with self.subTest(wylie=wylie):
                self._compare(wylie)
    
    # === PUNCTUATION ===
    
    def test_punctuation_marks(self):
        """Test Tibetan punctuation"""
        test_cases = [
            '/',      # ། shad
            '//',     # ༎ double shad
            '|',      # ༑ vertical shad
        ]
        
        for wylie in test_cases:
            with self.subTest(wylie=wylie):
                # Punctuation should preserve spaces
                self._compare(wylie, preserve_spaces=True)
    
    def test_punctuation_in_context(self):
        """Test punctuation with surrounding text"""
        # Punctuation alone
        simple_cases = [
            'ka/',       # ཀ།
            'ka//',      # ཀ༎
            'ka|',       # ཀ༑
        ]
        
        for wylie in simple_cases:
            with self.subTest(wylie=wylie):
                self._compare(wylie)
        
        # Punctuation with space after - pyewts DOES preserve space after punctuation
        self._compare('ka/ ki', preserve_spaces=True)
    
    # === NUMERALS ===
    
    def test_numerals(self):
        """Test Tibetan numerals"""
        test_cases = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '2020',  # ༢༠༢༠
            '108',   # ༡༠༨
        ]
        
        for wylie in test_cases:
            with self.subTest(wylie=wylie):
                self._compare(wylie)
    
    # === COMMON WORDS ===
    
    def test_common_tibetan_words(self):
        """Test common Tibetan words"""
        test_cases = [
            'bkra shis',      # བཀྲ་ཤིས (tashi)
            'sangs rgyas',    # སངས་རྒྱས (sangye/buddha)
            'byang chub',     # བྱང་ཆུབ (changchub)
            'sems dpa',       # སེམས་དཔའ (sempa)
            'chos',           # ཆོས (cho)
            'dkon mchog',     # དཀོན་མཆོག (konchok)
        ]
        
        for wylie in test_cases:
            with self.subTest(wylie=wylie):
                self._compare(wylie)


if __name__ == '__main__':
    unittest.main()

