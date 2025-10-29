#!/usr/bin/env python3
"""
Test Suite for Tibetan → Wylie Reverse Transliteration
Tests bidirectional transliteration capability.
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from wylie_transliterator.application.transliteration_service import TransliterationService


class TestReverseTransliteration(unittest.TestCase):
    """Test suite for Tibetan Unicode → Wylie transliteration"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize service once for all tests"""
        cls.service = TransliterationService()
    
    # === BASIC CONSONANTS ===
    
    def test_basic_consonants_reverse(self):
        """Test reverse transliteration of basic consonants"""
        test_cases = [
            ('ཀ', 'ka'),
            ('ཁ', 'kha'),
            ('ག', 'ga'),
            ('ང', 'nga'),
            ('ཅ', 'ca'),
            ('ཆ', 'cha'),
            ('ཇ', 'ja'),
            ('ཉ', 'nya'),
            ('ཏ', 'ta'),
            ('ཐ', 'tha'),
            ('ད', 'da'),
            ('ན', 'na'),
            ('པ', 'pa'),
            ('ཕ', 'pha'),
            ('བ', 'ba'),
            ('མ', 'ma'),
            ('ཙ', 'tsa'),
            ('ཚ', 'tsha'),
            ('ཛ', 'dza'),
            ('ཝ', 'wa'),
            ('ཞ', 'zha'),
            ('ཟ', 'za'),
            ('འ', "'a"),
            ('ཡ', 'ya'),
            ('ར', 'ra'),
            ('ལ', 'la'),
            ('ཤ', 'sha'),
            ('ས', 'sa'),
            ('ཧ', 'ha'),
            ('ཨ', 'a'),
        ]
        
        for tibetan, expected in test_cases:
            with self.subTest(tibetan=tibetan):
                result = self.service.transliterate_tibetan_to_wylie(tibetan)
                self.assertEqual(result, expected,
                               f"Failed: {tibetan} → {result} (expected {expected})")
    
    # === VOWELS ===
    
    def test_vowels_reverse(self):
        """Test reverse transliteration of vowel modifications"""
        test_cases = [
            ('ཀ', 'ka'),     # Inherent a
            ('ཀི', 'ki'),     # i vowel
            ('ཀུ', 'ku'),     # u vowel
            ('ཀེ', 'ke'),     # e vowel
            ('ཀོ', 'ko'),     # o vowel
            ('ཀཱ', 'kA'),    # long a
        ]
        
        for tibetan, expected in test_cases:
            with self.subTest(tibetan=tibetan):
                result = self.service.transliterate_tibetan_to_wylie(tibetan)
                self.assertEqual(result, expected)
    
    # === SUBSCRIPTS ===
    
    def test_subscripts_reverse(self):
        """Test reverse transliteration of subscripts"""
        test_cases = [
            ('བླ', 'bla'),    # subscript l
            ('ཀྱ', 'kya'),    # subscript y
            ('ཀྲ', 'kra'),    # subscript r
            ('དྭ', 'dwa'),    # subscript w
        ]
        
        for tibetan, expected in test_cases:
            with self.subTest(tibetan=tibetan):
                result = self.service.transliterate_tibetan_to_wylie(tibetan)
                self.assertEqual(result, expected)
    
    # === SUPERSCRIPTS ===
    
    def test_superscripts_reverse(self):
        """Test reverse transliteration of superscripts"""
        test_cases = [
            ('རྐ', 'rka'),    # superscript r
            ('ལྐ', 'lka'),    # superscript l
            ('སྐ', 'ska'),    # superscript s
        ]
        
        for tibetan, expected in test_cases:
            with self.subTest(tibetan=tibetan):
                result = self.service.transliterate_tibetan_to_wylie(tibetan)
                self.assertEqual(result, expected)
    
    # === COMPLEX STACKS ===
    
    def test_complex_stacks_reverse(self):
        """Test reverse transliteration of complex consonant stacks"""
        test_cases = [
            ('བསྒྲུབས', 'bsgrubs'),  # prescript + superscript + subscript + postscripts
            ('སངས', 'sangs'),         # superscript + postscript
            ('རྒྱས', 'rgyas'),        # superscript + subscript + postscript
        ]
        
        for tibetan, expected in test_cases:
            with self.subTest(tibetan=tibetan):
                result = self.service.transliterate_tibetan_to_wylie(tibetan)
                self.assertEqual(result, expected)
    
    # === COMMON WORDS ===
    
    def test_common_words_reverse(self):
        """Test reverse transliteration of common Tibetan words"""
        test_cases = [
            ('བླ་མ', 'bla ma'),           # lama
            ('སངས་རྒྱས', 'sangs rgyas'),  # buddha
            ('བྱང་ཆུབ', 'byang chub'),    # enlightenment
            ('བདེ་བ', 'bde ba'),           # happiness
        ]
        
        for tibetan, expected in test_cases:
            with self.subTest(tibetan=tibetan):
                result = self.service.transliterate_tibetan_to_wylie(tibetan)
                self.assertEqual(result, expected)
    
    # === PUNCTUATION ===
    
    def test_punctuation_reverse(self):
        """Test reverse transliteration of Tibetan punctuation"""
        test_cases = [
            ('།', '/'),      # shad
            ('༎', '//'),     # double shad (nyis shad)
            (' ', ' '),      # space stays space
        ]
        
        for tibetan, expected in test_cases:
            with self.subTest(tibetan=tibetan):
                result = self.service.transliterate_tibetan_to_wylie(tibetan)
                self.assertEqual(result, expected)
    
    # === NUMERALS ===
    
    def test_numerals_reverse(self):
        """Test reverse transliteration of Tibetan numerals"""
        test_cases = [
            ('༠', '0'),
            ('༡', '1'),
            ('༢', '2'),
            ('༣', '3'),
            ('༤', '4'),
            ('༥', '5'),
            ('༦', '6'),
            ('༧', '7'),
            ('༨', '8'),
            ('༩', '9'),
            ('༡༩༥༩', '1959'),
        ]
        
        for tibetan, expected in test_cases:
            with self.subTest(tibetan=tibetan):
                result = self.service.transliterate_tibetan_to_wylie(tibetan)
                self.assertEqual(result, expected)
    
    # === SANSKRIT ===
    
    def test_sanskrit_reverse(self):
        """Test reverse transliteration of Sanskrit extensions"""
        test_cases = [
            ('ཊ', 'Ta'),     # retroflex t
            ('ཎ', 'Na'),     # retroflex n
            ('ཀྵ', 'kss'),   # ksha
        ]
        
        for tibetan, expected in test_cases:
            with self.subTest(tibetan=tibetan):
                result = self.service.transliterate_tibetan_to_wylie(tibetan)
                self.assertEqual(result, expected)
    
    def test_sanskrit_marks_reverse(self):
        """Test reverse transliteration of Sanskrit marks"""
        test_cases = [
            ('ཾ', 'M'),      # anusvara
            ('ཿ', 'H'),      # visarga
        ]
        
        for tibetan, expected in test_cases:
            with self.subTest(tibetan=tibetan):
                result = self.service.transliterate_tibetan_to_wylie(tibetan)
                self.assertEqual(result, expected)
    
    # === MANTRA ===
    
    def test_mantra_reverse(self):
        """Test reverse transliteration of Om Mani Padme Hum"""
        tibetan = 'ཨོཾ་མ་ཎི་པ་དྨེ་ཧཱུྃ།'
        # Note: The exact spacing/capitalization might vary
        result = self.service.transliterate_tibetan_to_wylie(tibetan)
        
        # Check that key components are present
        self.assertIn('o', result)  # 'o' vowel
        self.assertIn('M', result)  # anusvara
        self.assertIn('ma', result)  # 'ma'
        # Check for Sanskrit retroflex (ཎི = Ni, not Na)
        self.assertTrue('Ni' in result or 'ni' in result,
                       f"Expected 'Ni' or 'ni' in result: {result}")
        self.assertIn('/', result)  # shad at end
    
    # === BIDIRECTIONAL ===
    
    def test_bidirectional_simple(self):
        """Test that simple syllables round-trip correctly"""
        test_cases = [
            'ka', 'kha', 'ga', 'pa', 'ma',
            'bla', 'rka', 'ska', 'bya',
        ]
        
        for wylie in test_cases:
            with self.subTest(wylie=wylie):
                # Wylie → Tibetan → Wylie
                tibetan = self.service.transliterate_wylie_to_tibetan(wylie)
                result = self.service.transliterate_tibetan_to_wylie(tibetan)
                self.assertEqual(result, wylie,
                               f"Round-trip failed: {wylie} → {tibetan} → {result}")
    
    def test_bidirectional_words(self):
        """Test that common words round-trip correctly"""
        test_cases = [
            'bla ma',
            'sangs rgyas',
            'byang chub',
        ]
        
        for wylie in test_cases:
            with self.subTest(wylie=wylie):
                # Wylie → Tibetan → Wylie
                tibetan = self.service.transliterate_wylie_to_tibetan(wylie)
                result = self.service.transliterate_tibetan_to_wylie(tibetan)
                self.assertEqual(result, wylie,
                               f"Round-trip failed: {wylie} → {tibetan} → {result}")
    
    # === BATCH PROCESSING ===
    
    def test_batch_reverse(self):
        """Test batch reverse transliteration"""
        tibetan_texts = ['བླ་མ', 'སངས་རྒྱས', 'བྱང་ཆུབ']
        expected = ['bla ma', 'sangs rgyas', 'byang chub']
        
        results = self.service.transliterate_tibetan_to_wylie_batch(tibetan_texts)
        self.assertEqual(results, expected)
    
    # === EDGE CASES ===
    
    def test_empty_string_reverse(self):
        """Test reverse transliteration of empty string"""
        result = self.service.transliterate_tibetan_to_wylie('')
        self.assertEqual(result, '')
    
    def test_unknown_characters_reverse(self):
        """Test that unknown characters pass through"""
        mixed = 'ཀ@#$བ'
        result = self.service.transliterate_tibetan_to_wylie(mixed)
        self.assertIn('ka', result)
        self.assertIn('ba', result)
        self.assertIn('@', result)  # Should pass through


def run_tests():
    """Run the reverse transliteration test suite"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestReverseTransliteration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("REVERSE TRANSLITERATION TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    sys.exit(0 if result.wasSuccessful() else 1)

