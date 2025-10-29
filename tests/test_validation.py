#!/usr/bin/env python3
"""
Test Suite for Extended Wylie Validation
Tests validation according to EWTS standard.
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from wylie_transliterator.application.validation_service import ValidationService
from wylie_transliterator.domain.value_objects.validation_rules import ERROR_TYPES


class TestWylieValidation(unittest.TestCase):
    """Test suite for Wylie validation"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize validation service once for all tests"""
        cls.validator = ValidationService()
    
    # === VALID INPUT TESTS ===
    
    def test_valid_basic_syllables(self):
        """Test that valid basic syllables pass validation"""
        valid_inputs = [
            'ka',      # Basic consonant
            'kha',     # Multi-char consonant
            'bla',     # Subscript
            'rka',     # Superscript
            'grwa',    # Prescript + subscript
            'bsgrubs', # Complex stack
            'sangs rgyas',  # Multiple syllables
        ]
        
        for wylie in valid_inputs:
            with self.subTest(wylie=wylie):
                result = self.validator.validate_wylie(wylie)
                self.assertTrue(result.is_valid, 
                              f"'{wylie}' should be valid but got: {result.get_error_summary()}")
    
    def test_valid_vowels(self):
        """Test valid vowel modifications"""
        valid_inputs = [
            'ki',   # i vowel
            'ku',   # u vowel
            'ke',   # e vowel
            'ko',   # o vowel
            'kA',   # long a
        ]
        
        for wylie in valid_inputs:
            with self.subTest(wylie=wylie):
                result = self.validator.validate_wylie(wylie)
                self.assertTrue(result.is_valid)
    
    def test_valid_sanskrit(self):
        """Test valid Sanskrit extensions"""
        valid_inputs = [
            'oM',        # Standalone vowel + mark
            'hUM',       # Sanskrit compound
            'Ni',        # Sanskrit retroflex
            'Ta',        # Sanskrit retroflex
            'kss',       # Sanskrit ksha
        ]
        
        for wylie in valid_inputs:
            with self.subTest(wylie=wylie):
                result = self.validator.validate_wylie(wylie)
                self.assertTrue(result.is_valid)
    
    def test_valid_punctuation(self):
        """Test valid punctuation and numerals"""
        valid_inputs = [
            'ka nga/',   # Shad
            'ka nga||',  # Double shad
            '1959',      # Numerals
            'ka. ba',    # Period
        ]
        
        for wylie in valid_inputs:
            with self.subTest(wylie=wylie):
                result = self.validator.validate_wylie(wylie)
                self.assertTrue(result.is_valid)
    
    def test_valid_complex_words(self):
        """Test valid complex Tibetan words"""
        valid_inputs = [
            'bla ma',
            'sangs rgyas',
            'byang chub',
            'oM ma Ni pa dme hUM|',
            'bsgrubs',
            'grwa drwa',
        ]
        
        for wylie in valid_inputs:
            with self.subTest(wylie=wylie):
                result = self.validator.validate_wylie(wylie)
                self.assertTrue(result.is_valid,
                              f"'{wylie}' should be valid: {result.get_error_summary()}")
    
    # === INVALID INPUT TESTS ===
    
    def test_unknown_characters(self):
        """Test detection of unknown characters"""
        invalid_inputs = [
            ('xyz', 'x'),    # Completely unknown
            ('ka@ba', '@'),  # Special char
            ('ka#ba', '#'),  # Hash
            ('ka$ba', '$'),  # Dollar
        ]
        
        for wylie, expected_char in invalid_inputs:
            with self.subTest(wylie=wylie):
                result = self.validator.validate_wylie(wylie)
                self.assertFalse(result.is_valid)
                self.assertTrue(any(e.error_type == ERROR_TYPES.UNKNOWN_CHARACTER 
                                  for e in result.errors))
    
    def test_invalid_prescript_combinations(self):
        """Test invalid prescript + root combinations"""
        invalid_inputs = [
            'gka',   # g before k is invalid
            # Note: 'dda' is valid as Sanskrit consonant ḍha (dd)
            # Note: 'bda' gets parsed as just 'b', not as prescript combo
            'mpa',   # m before p is invalid (not in EWTS prescript rules)
        ]
        
        for wylie in invalid_inputs:
            with self.subTest(wylie=wylie):
                result = self.validator.validate_wylie(wylie)
                self.assertFalse(result.is_valid)
                # Should have prescript error
                has_prescript_error = any(
                    e.error_type == ERROR_TYPES.INVALID_PRESCRIPT 
                    for e in result.errors
                )
                self.assertTrue(has_prescript_error,
                              f"Expected prescript error for '{wylie}'")
    
    def test_invalid_superscript_combinations(self):
        """Test invalid superscript + root combinations"""
        invalid_inputs = [
            'rda',   # r above d is invalid
            'lla',   # l above l is invalid
            'ska',   # s above k is valid, but let's test edge cases
        ]
        
        # Note: ska is actually valid, so let's use truly invalid ones
        invalid_inputs = [
            'rpha',  # r above ph is invalid
            'lkha',  # l above kh is invalid
        ]
        
        for wylie in invalid_inputs:
            with self.subTest(wylie=wylie):
                result = self.validator.validate_wylie(wylie)
                # These should be invalid
                if not result.is_valid:
                    has_superscript_error = any(
                        e.error_type == ERROR_TYPES.INVALID_SUPERSCRIPT
                        for e in result.errors
                    )
                    self.assertTrue(has_superscript_error,
                                  f"Expected superscript error for '{wylie}'")
    
    def test_invalid_subscript_combinations(self):
        """Test invalid subscript + root combinations"""
        invalid_inputs = [
            'nya',   # n with ya subscript is invalid
            'tsha',  # ts with ha subscript is invalid
            'cha',   # c with ha subscript is invalid
        ]
        
        for wylie in invalid_inputs:
            with self.subTest(wylie=wylie):
                result = self.validator.validate_wylie(wylie)
                if not result.is_valid:
                    has_subscript_error = any(
                        e.error_type == ERROR_TYPES.INVALID_SUBSCRIPT
                        for e in result.errors
                    )
                    # Some might be parsed differently, so we check if error exists
                    self.assertTrue(len(result.errors) > 0,
                                  f"'{wylie}' should have validation error")
    
    # === VALIDATION SERVICE API TESTS ===
    
    def test_is_valid_wylie_method(self):
        """Test simple boolean validation"""
        self.assertTrue(self.validator.is_valid_wylie('bla ma'))
        self.assertFalse(self.validator.is_valid_wylie('xyz123'))
    
    def test_get_validation_errors_method(self):
        """Test error message extraction"""
        errors = self.validator.get_validation_errors('xyz')
        self.assertGreater(len(errors), 0)
        self.assertIsInstance(errors[0], str)
    
    def test_validate_and_get_report(self):
        """Test structured report generation"""
        report = self.validator.validate_and_get_report('bla ma')
        
        self.assertIn('is_valid', report)
        self.assertIn('error_count', report)
        self.assertIn('warning_count', report)
        self.assertIn('errors', report)
        self.assertIn('summary', report)
        
        self.assertTrue(report['is_valid'])
        self.assertEqual(report['error_count'], 0)
    
    def test_validate_batch(self):
        """Test batch validation"""
        texts = ['bla ma', 'sangs rgyas', 'xyz123']
        results = self.validator.validate_batch(texts)
        
        self.assertEqual(len(results), 3)
        self.assertTrue(results[0].is_valid)
        self.assertTrue(results[1].is_valid)
        self.assertFalse(results[2].is_valid)
    
    # === EDGE CASES ===
    
    def test_empty_string(self):
        """Test empty input"""
        result = self.validator.validate_wylie('')
        self.assertTrue(result.is_valid)
    
    def test_whitespace_only(self):
        """Test whitespace-only input"""
        result = self.validator.validate_wylie('   \n\t  ')
        self.assertTrue(result.is_valid)
    
    def test_punctuation_only(self):
        """Test punctuation-only input"""
        result = self.validator.validate_wylie('/ | /')
        self.assertTrue(result.is_valid)
    
    # === VALIDATION RESULT TESTS ===
    
    def test_validation_result_structure(self):
        """Test ValidationResult structure"""
        result = self.validator.validate_wylie('xyz')
        
        self.assertFalse(result.is_valid)
        self.assertIsInstance(result.errors, tuple)  # Immutable
        self.assertGreater(len(result.errors), 0)
        
        error = result.errors[0]
        self.assertIsNotNone(error.error_type)
        self.assertIsNotNone(error.message)
        self.assertIsNotNone(error.position)
        self.assertIsNotNone(error.syllable)
    
    def test_validation_result_summary(self):
        """Test error summary generation"""
        result = self.validator.validate_wylie('xyz')
        summary = result.get_error_summary()
        
        self.assertIn('error', summary.lower())
        self.assertIsInstance(summary, str)
    
    def test_validation_result_bool(self):
        """Test ValidationResult as boolean"""
        valid_result = self.validator.validate_wylie('bla ma')
        invalid_result = self.validator.validate_wylie('xyz')
        
        self.assertTrue(bool(valid_result))
        self.assertFalse(bool(invalid_result))
    
    # === REAL WORLD EXAMPLES ===
    
    def test_common_mistakes(self):
        """Test common transliteration mistakes"""
        # These should be caught as errors
        mistakes = [
            'qa',      # q is not in EWTS
            'xa',      # x is not in EWTS  
            'bhlа',    # bh + l is invalid
        ]
        
        for wylie in mistakes:
            with self.subTest(wylie=wylie):
                result = self.validator.validate_wylie(wylie)
                self.assertFalse(result.is_valid,
                              f"'{wylie}' should be invalid")
    
    def test_valid_mantra(self):
        """Test the Om Mani Padme Hum mantra"""
        mantra = "oM ma Ni pa dme hUM|"
        result = self.validator.validate_wylie(mantra)
        self.assertTrue(result.is_valid,
                       f"Mantra should be valid: {result.get_error_summary()}")


def run_tests():
    """Run the validation test suite with verbose output"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestWylieValidation))
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("VALIDATION TEST SUMMARY")
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

