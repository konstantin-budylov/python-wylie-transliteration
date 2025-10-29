#!/usr/bin/env python3
"""
Comprehensive Test Suite for Wylie Transliterator
Tests based on THL Extended Wylie Transliteration Scheme (EWTS)
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from wylie_transliterator.application.transliteration_service import TransliterationService
from wylie_transliterator.domain.models.syllable import SyllableComponents

# Backward compatibility wrapper
class WylieTransliterator:
    """Compatibility wrapper for existing tests"""
    def __init__(self):
        self.service = TransliterationService()
    
    def transliterate(self, text, spaces_as_tsheg=True):
        return self.service.transliterate_wylie_to_tibetan(text, preserve_spaces=not spaces_as_tsheg)


class TestWylieTransliterator(unittest.TestCase):
    """Test suite for Wylie to Tibetan transliteration"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize transliterator once for all tests"""
        cls.trans = WylieTransliterator()
    
    # === BASIC CONSONANTS ===
    
    def test_basic_consonants(self):
        """Test all 30 basic Tibetan consonants"""
        test_cases = [
            ('ka', 'ཀ'),
            ('kha', 'ཁ'),
            ('ga', 'ག'),
            ('nga', 'ང'),
            ('ca', 'ཅ'),
            ('cha', 'ཆ'),
            ('ja', 'ཇ'),
            ('nya', 'ཉ'),
            ('ta', 'ཏ'),
            ('tha', 'ཐ'),
            ('da', 'ད'),
            ('na', 'ན'),
            ('pa', 'པ'),
            ('pha', 'ཕ'),
            ('ba', 'བ'),
            ('ma', 'མ'),
            ('tsa', 'ཙ'),
            ('tsha', 'ཚ'),
            ('dza', 'ཛ'),
            ('wa', 'ཝ'),
            ('zha', 'ཞ'),
            ('za', 'ཟ'),
            ("'a", 'འ'),  # a-chung
            ('ya', 'ཡ'),
            ('ra', 'ར'),
            ('la', 'ལ'),
            ('sha', 'ཤ'),
            ('sa', 'ས'),
            ('ha', 'ཧ'),
            ('a', 'ཨ'),    # pure vowel a
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected, 
                               f"Failed: {wylie} -> expected {expected}, got {result}")
    
    def test_aspirated_consonants(self):
        """Test aspirated consonants"""
        test_cases = [
            ('kha', 'ཁ'),
            ('cha', 'ཆ'),
            ('tha', 'ཐ'),
            ('pha', 'ཕ'),
            ('tsha', 'ཚ'),
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    # === VOWELS ===
    
    def test_vowels(self):
        """Test all 5 vowel modifications"""
        test_cases = [
            ('ka', 'ཀ'),    # inherent 'a' (not written)
            ('ki', 'ཀི'),
            ('ku', 'ཀུ'),
            ('ke', 'ཀེ'),
            ('ko', 'ཀོ'),
            ('kA', 'ཀཱ'),   # long 'a'
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    def test_inherent_vowel(self):
        """Test that inherent 'a' is not written"""
        # 'a' is inherent, should not produce vowel sign
        result = self.trans.transliterate('ka')
        self.assertEqual(result, 'ཀ')
        self.assertNotIn('\u0F71', result)  # Should NOT have AA sign
    
    # === SUBSCRIPTS (STACKS) ===
    
    def test_subscripts_r(self):
        """Test subscript 'r' combinations"""
        test_cases = [
            ('kra', 'ཀྲ'),
            ('gra', 'གྲ'),
            ('pra', 'པྲ'),
            ('bra', 'བྲ'),
            ('mra', 'མྲ'),
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    def test_subscripts_l(self):
        """Test subscript 'l' combinations"""
        test_cases = [
            ('kla', 'ཀླ'),
            ('gla', 'གླ'),
            ('bla', 'བླ'),
            ('zla', 'ཟླ'),
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    def test_subscripts_y(self):
        """Test subscript 'y' combinations"""
        test_cases = [
            ('kya', 'ཀྱ'),
            ('gya', 'གྱ'),
            ('pya', 'པྱ'),
            ('phya', 'ཕྱ'),
            ('bya', 'བྱ'),
            ('mya', 'མྱ'),
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    def test_subscripts_w(self):
        """Test subscript 'w' combinations"""
        test_cases = [
            ('kwa', 'ཀྭ'),
            ('gwa', 'གྭ'),
            ('twa', 'ཏྭ'),
            ('dwa', 'དྭ'),
            ('tswa', 'ཙྭ'),
            ('zhwa', 'ཞྭ'),
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    # === SUPERSCRIPTS ===
    
    def test_superscript_r(self):
        """Test superscript 'r' combinations"""
        test_cases = [
            ('rka', 'རྐ'),
            ('rga', 'རྒ'),
            ('rnga', 'རྔ'),
            ('rja', 'རྗ'),
            ('rnya', 'རྙ'),
            ('rta', 'རྟ'),
            ('rda', 'རྡ'),
            ('rna', 'རྣ'),
            ('rba', 'རྦ'),
            ('rma', 'རྨ'),
            ('rtsa', 'རྩ'),
            ('rdza', 'རྫ'),
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    def test_superscript_l(self):
        """Test superscript 'l' combinations"""
        test_cases = [
            ('lka', 'ལྐ'),
            ('lga', 'ལྒ'),
            ('lnga', 'ལྔ'),
            ('lca', 'ལྕ'),
            ('lja', 'ལྗ'),
            ('lta', 'ལྟ'),
            ('lda', 'ལྡ'),
            ('lpa', 'ལྤ'),
            ('lba', 'ལྦ'),
            ('lha', 'ལྷ'),
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    def test_superscript_s(self):
        """Test superscript 's' combinations"""
        test_cases = [
            ('ska', 'སྐ'),
            ('sga', 'སྒ'),
            ('snga', 'སྔ'),
            ('snya', 'སྙ'),
            ('sta', 'སྟ'),
            ('sda', 'སྡ'),
            ('sna', 'སྣ'),
            ('spa', 'སྤ'),
            ('sba', 'སྦ'),
            ('sma', 'སྨ'),
            ('stsa', 'སྩ'),
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    # === PRESCRIPTS ===
    
    def test_prescripts(self):
        """Test prescript combinations"""
        test_cases = [
            ('dka', 'དཀ'),
            ('dga', 'དག'),
            ('bka', 'བཀ'),
            ('bga', 'བག'),
            ('mda', 'མད'),
            ('mna', 'མན'),
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    # === POSTSCRIPTS ===
    
    def test_postscripts_single(self):
        """Test single postscripts"""
        test_cases = [
            ('kag', 'ཀག'),
            ('kang', 'ཀང'),
            ('kad', 'ཀད'),
            ('kan', 'ཀན'),
            ('kab', 'ཀབ'),
            ('kam', 'ཀམ'),
            ('kar', 'ཀར'),
            ('kal', 'ཀལ'),
            ('kas', 'ཀས'),
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    def test_postscripts_double(self):
        """Test double postscripts"""
        test_cases = [
            ('kags', 'ཀགས'),
            ('kangs', 'ཀངས'),
            ('kabs', 'ཀབས'),
            ('kams', 'ཀམས'),
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    # === COMPLEX STACKS ===
    
    def test_complex_stacks_from_thl(self):
        """Test complex stacks from THL EWTS examples"""
        test_cases = [
            # From THL specification examples
            ('bsgrubs', 'བསྒྲུབས'),  # b + s + g + r + u + b + s
            ('skra', 'སྐྲ'),          # s + k + r + a
            ('bskyed', 'བསྐྱེད'),     # b + s + k + y + e + d
            ('spyod', 'སྤྱོད'),       # s + p + y + o + d
            ('rgyal', 'རྒྱལ'),       # r + g + y + a + l
            ('dbyar', 'དབྱར'),       # d + b + y + a + r
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected,
                               f"Complex stack failed: {wylie}")
    
    def test_superscript_with_subscript(self):
        """Test combinations of superscript + subscript"""
        test_cases = [
            ('rkya', 'རྐྱ'),
            ('rgya', 'རྒྱ'),
            ('rmya', 'རྨྱ'),
            ('rgwa', 'རྒྭ'),
            ('rtswa', 'རྩྭ'),
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    def test_double_subscripts(self):
        """Test rare double subscripts (r+w combinations)"""
        test_cases = [
            ('grwa', 'གྲྭ'),
            ('drwa', 'དྲྭ'),
            ('phywa', 'ཕྱྭ'),
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    # === COMMON WORDS ===
    
    def test_common_tibetan_words(self):
        """Test common Tibetan words"""
        test_cases = [
            ('dbu', 'དབུ'),           # head, top
            ('bla ma', 'བླ་མ'),       # guru (with tsheg)
            ('rgyal ba', 'རྒྱལ་བ'),   # victor, buddha
            ('chos', 'ཆོས'),          # dharma
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    # === NUMERALS ===
    
    def test_numerals(self):
        """Test Tibetan numerals 0-9"""
        test_cases = [
            ('0', '༠'),
            ('1', '༡'),
            ('2', '༢'),
            ('3', '༣'),
            ('4', '༤'),
            ('5', '༥'),
            ('6', '༦'),
            ('7', '༧'),
            ('8', '༨'),
            ('9', '༩'),
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    def test_multi_digit_numbers(self):
        """Test multi-digit numbers"""
        test_cases = [
            ('1959', '༡༩༥༩'),
            ('2024', '༢༠༢༤'),
            ('108', '༡༠༨'),
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    # === PUNCTUATION ===
    
    def test_tsheg_separator(self):
        """Test tsheg (syllable separator) from space"""
        result = self.trans.transliterate('bla ma', spaces_as_tsheg=True)
        self.assertEqual(result, 'བླ་མ')
        self.assertIn('་', result)  # tsheg present
    
    def test_shad_marks(self):
        """Test shad punctuation marks"""
        test_cases = [
            ('/', '།'),    # shad
            ('//', '༎'),  # double shad
            ('|', '།'),    # alternative notation
            ('||', '༎'),  # alternative notation
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    # === SANSKRIT EXTENSIONS ===
    
    def test_sanskrit_marks(self):
        """Test Sanskrit anusvara and visarga"""
        test_cases = [
            ('M', 'ཾ'),    # anusvara
            ('H', 'ཿ'),    # visarga
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)
    
    def test_sanskrit_in_context(self):
        """Test Sanskrit marks and mantras"""
        # Individual syllables from Om Mani Padme Hum mantra
        test_cases = [
            ('oM', 'ཨོཾ'),      # Standalone vowel + anusvara
            ('ma', 'མ'),        # Basic syllable
            ('Ni', 'ཎི'),       # Sanskrit retroflex ṇ
            ('pa', 'པ'),        # Basic syllable
            ('dme', 'དྨེ'),     # Subscript m
            ('hUM', 'ཧཱུྃ'),    # Compound vowel + special anusvara
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected, 
                                f"Failed: {wylie} → {result} (expected {expected})")
    
    def test_full_mantra(self):
        """Test the complete Om Mani Padme Hum mantra"""
        wylie = "oM ma Ni pa dme hUM|"
        expected = "ཨོཾ་མ་ཎི་པ་དྨེ་ཧཱུྃ།"
        result = self.trans.transliterate(wylie)
        self.assertEqual(result, expected,
                        f"\nInput:    {wylie}\nResult:   {result}\nExpected: {expected}")
    
    # === EDGE CASES ===
    
    def test_empty_string(self):
        """Test empty input"""
        result = self.trans.transliterate('')
        self.assertEqual(result, '')
    
    def test_unknown_characters(self):
        """Test that unknown characters pass through"""
        result = self.trans.transliterate('ka@#$ba')
        self.assertIn('ཀ', result)
        self.assertIn('བ', result)
    
    def test_mixed_content(self):
        """Test mixed Tibetan and punctuation"""
        result = self.trans.transliterate('ka nga/ da ma||')
        self.assertIn('ཀ', result)
        self.assertIn('ང', result)
        self.assertIn('།', result)  # shad
        self.assertIn('༎', result)  # double shad
    
    # === CASE SENSITIVITY ===
    
    def test_case_insensitive_basic(self):
        """Test that basic consonants are case-insensitive"""
        # Lowercase
        result1 = self.trans.transliterate('ka')
        # Uppercase (should give same result for basic letters)
        result2 = self.trans.transliterate('KA')
        # Both should produce ཀ + inherent a
        self.assertEqual(result1, result2)
    
    # === REGRESSION TESTS (from Perl code analysis) ===
    
    def test_perl_example_bsgrubs(self):
        """Test the example from Perl README: bsgrubs"""
        result = self.trans.transliterate('bsgrubs')
        expected = 'བསྒྲུབས'
        self.assertEqual(result, expected,
                        "Perl example 'bsgrubs' failed")
    
    def test_thl_standard_examples(self):
        """Test examples from THL EWTS standard document"""
        test_cases = [
            ('rka rga rnga', 'རྐ་རྒ་རྔ'),
            ('lka lga lnga', 'ལྐ་ལྒ་ལྔ'),
            ('ska sga snga', 'སྐ་སྒ་སྔ'),
            ('kya khya gya', 'ཀྱ་ཁྱ་གྱ'),
            ('kra khra gra', 'ཀྲ་ཁྲ་གྲ'),
            ('kla gla bla', 'ཀླ་གླ་བླ'),
        ]
        
        for wylie, expected in test_cases:
            with self.subTest(wylie=wylie):
                result = self.trans.transliterate(wylie)
                self.assertEqual(result, expected)


class TestSyllableComponents(unittest.TestCase):
    """Test the syllable component parsing"""
    
    def test_simple_syllable(self):
        """Test parsing a simple syllable"""
        # Internal parsing is now encapsulated - test functional behavior instead
        trans = WylieTransliterator()
        result = trans.transliterate('ka')
        self.assertEqual(result, 'ཀ')
    
    def test_complex_syllable(self):
        """Test parsing a complex syllable like 'bsgrubs'"""
        # Internal parsing is now encapsulated - test functional behavior instead
        trans = WylieTransliterator()
        result = trans.transliterate('bsgrubs')
        self.assertEqual(result, 'བསྒྲུབས')


def run_test_suite():
    """Run the complete test suite with verbose output"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestWylieTransliterator))
    suite.addTests(loader.loadTestsFromTestCase(TestSyllableComponents))
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_test_suite()
    sys.exit(0 if success else 1)

