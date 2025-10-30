"""
Tests for ACIP (Asian Classics Input Project) transliteration.

These tests verify bidirectional conversion between ACIP, EWTS, and Tibetan Unicode.
"""

import unittest
from src.wylie_transliterator.application.acip_service import ACIPService
from src.wylie_transliterator.domain.services.acip_converter import ACIPConverter


class TestACIPToEWTS(unittest.TestCase):
    """Test ACIP to EWTS conversion."""
    
    def setUp(self):
        self.converter = ACIPConverter()
    
    def test_simple_word(self):
        """Test simple ACIP word conversion."""
        self.assertEqual(
            self.converter.acip_to_ewts("BSGRUBS"),
            "bsgrubs"
        )
    
    def test_with_vowel(self):
        """Test ACIP with vowel."""
        self.assertEqual(
            self.converter.acip_to_ewts("BA'I"),
            "ba'i"
        )
    
    def test_compound_word(self):
        """Test compound ACIP word."""
        self.assertEqual(
            self.converter.acip_to_ewts("KHAMS"),
            "khams"
        )
    
    def test_ts_tsh_distinction(self):
        """Test TS/TZ distinction in ACIP."""
        # ACIP TS = EWTS tsh
        self.assertEqual(
            self.converter.acip_to_ewts("TSA"),
            "tsha"
        )
        # ACIP TZ = EWTS ts
        self.assertEqual(
            self.converter.acip_to_ewts("TZA"),
            "tsa"
        )
    
    def test_reverse_vowel(self):
        """Test ACIP 'i' (reverse vowel)."""
        # ACIP i = EWTS -I
        self.assertEqual(
            self.converter.acip_to_ewts("L'i"),
            "l-I"
        )
    
    def test_diphthongs(self):
        """Test ACIP diphthongs."""
        # ACIP EE = EWTS ai
        self.assertEqual(
            self.converter.acip_to_ewts("AEE"),
            "ai"
        )
        # ACIP OO = EWTS au
        self.assertEqual(
            self.converter.acip_to_ewts("AOO"),
            "au"
        )
    
    def test_stacked_consonants(self):
        """Test complex stacked consonants."""
        self.assertEqual(
            self.converter.acip_to_ewts("DRA"),
            "dra"
        )
        self.assertEqual(
            self.converter.acip_to_ewts("BSGRVUBS"),
            "bsgrwubs"
        )
    
    def test_sanskrit_stack(self):
        """Test Sanskrit consonant stack with +."""
        # Sanskrit needs explicit +
        self.assertEqual(
            self.converter.acip_to_ewts("PAn+dI"),
            "paN+Di"
        )
    
    def test_complex_sentence(self):
        """Test complete ACIP sentence."""
        acip = "BLA MA"
        ewts = self.converter.acip_to_ewts(acip)
        # Should convert to lowercase with proper spacing
        self.assertIn("bla", ewts.lower())
        self.assertIn("ma", ewts.lower())


class TestEWTSToACIP(unittest.TestCase):
    """Test EWTS to ACIP conversion."""
    
    def setUp(self):
        self.converter = ACIPConverter()
    
    def test_simple_reverse(self):
        """Test simple EWTS to ACIP."""
        self.assertEqual(
            self.converter.ewts_to_acip("bsgrubs"),
            "BSGRUBS"
        )
    
    def test_with_vowel_reverse(self):
        """Test EWTS with vowel to ACIP."""
        self.assertEqual(
            self.converter.ewts_to_acip("ba'i"),
            "BA'I"
        )
    
    def test_tsh_to_ts(self):
        """Test EWTS tsh to ACIP TS."""
        result = self.converter.ewts_to_acip("tsha")
        self.assertIn("TS", result.upper())
    
    def test_ts_to_tz(self):
        """Test EWTS ts to ACIP TZ."""
        result = self.converter.ewts_to_acip("tsa")
        self.assertIn("TZ", result.upper())
    
    def test_reverse_vowel_reverse(self):
        """Test EWTS -I to ACIP i."""
        result = self.converter.ewts_to_acip("l-I")
        self.assertIn("'i", result.lower())
    
    def test_diphthongs_reverse(self):
        """Test EWTS diphthongs to ACIP."""
        self.assertIn("EE", self.converter.ewts_to_acip("ai").upper())
        self.assertIn("OO", self.converter.ewts_to_acip("au").upper())


class TestACIPToUnicode(unittest.TestCase):
    """Test ACIP to Tibetan Unicode conversion."""
    
    def setUp(self):
        self.service = ACIPService()
    
    def test_simple_word_to_unicode(self):
        """Test simple ACIP to Unicode."""
        result = self.service.acip_to_unicode("BSGRUBS")
        self.assertEqual(result, "བསྒྲུབས")
    
    def test_two_words_to_unicode(self):
        """Test two-word ACIP to Unicode."""
        result = self.service.acip_to_unicode("BLA MA")
        self.assertEqual(result, "བླ་མ")
    
    def test_buddha_to_unicode(self):
        """Test 'Buddha' in ACIP to Unicode."""
        result = self.service.acip_to_unicode("SANGS RGYAS")
        self.assertEqual(result, "སངས་རྒྱས")
    
    def test_enlightenment_to_unicode(self):
        """Test 'Enlightenment' in ACIP to Unicode."""
        result = self.service.acip_to_unicode("BYANG CHUB")
        self.assertEqual(result, "བྱང་ཆུབ")
    
    def test_with_vowel_marks_to_unicode(self):
        """Test ACIP with vowel marks to Unicode."""
        result = self.service.acip_to_unicode("KI")
        self.assertEqual(result, "ཀི")
        
        result = self.service.acip_to_unicode("KU")
        self.assertEqual(result, "ཀུ")
    
    def test_sanskrit_to_unicode(self):
        """Test Sanskrit ACIP to Unicode."""
        result = self.service.acip_to_unicode("DHA")
        # Should convert to Tibetan Unicode (contains Tibetan character)
        self.assertTrue(any('\u0F00' <= c <= '\u0FFF' for c in result))
        # Should produce valid output (not empty)
        self.assertTrue(len(result) > 0)


class TestUnicodeToACIP(unittest.TestCase):
    """Test Tibetan Unicode to ACIP conversion."""
    
    def setUp(self):
        self.service = ACIPService()
    
    def test_simple_unicode_to_acip(self):
        """Test simple Unicode to ACIP."""
        result = self.service.unicode_to_acip("བསྒྲུབས")
        self.assertEqual(result, "BSGRUBS")
    
    def test_two_words_unicode_to_acip(self):
        """Test two-word Unicode to ACIP."""
        result = self.service.unicode_to_acip("བླ་མ")
        self.assertEqual(result, "BLA MA")
    
    def test_buddha_unicode_to_acip(self):
        """Test 'Buddha' Unicode to ACIP."""
        result = self.service.unicode_to_acip("སངས་རྒྱས")
        self.assertEqual(result, "SANGS RGYAS")
    
    def test_vowel_marks_unicode_to_acip(self):
        """Test Unicode with vowel marks to ACIP."""
        result = self.service.unicode_to_acip("ཀི")
        self.assertEqual(result, "KI")


class TestACIPBatchOperations(unittest.TestCase):
    """Test batch ACIP operations."""
    
    def setUp(self):
        self.service = ACIPService()
    
    def test_batch_acip_to_unicode(self):
        """Test batch conversion from ACIP to Unicode."""
        acip_texts = ["BSGRUBS", "BLA MA", "SANGS RGYAS"]
        results = self.service.acip_to_unicode_batch(acip_texts)
        
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0], "བསྒྲུབས")
        self.assertEqual(results[1], "བླ་མ")
        self.assertEqual(results[2], "སངས་རྒྱས")
    
    def test_batch_unicode_to_acip(self):
        """Test batch conversion from Unicode to ACIP."""
        unicode_texts = ["བསྒྲུབས", "བླ་མ", "སངས་རྒྱས"]
        results = self.service.unicode_to_acip_batch(unicode_texts)
        
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0], "BSGRUBS")
        self.assertEqual(results[1], "BLA MA")
        self.assertEqual(results[2], "SANGS RGYAS")


class TestACIPFormatDetection(unittest.TestCase):
    """Test format auto-detection."""
    
    def setUp(self):
        self.service = ACIPService()
    
    def test_detect_acip(self):
        """Test detection of ACIP format."""
        self.assertEqual(
            self.service.detect_format("BSGRUBS"),
            'acip'
        )
        self.assertEqual(
            self.service.detect_format("BLA MA"),
            'acip'
        )
    
    def test_detect_ewts(self):
        """Test detection of EWTS format."""
        self.assertEqual(
            self.service.detect_format("bsgrubs"),
            'ewts'
        )
        self.assertEqual(
            self.service.detect_format("bla ma"),
            'ewts'
        )
    
    def test_detect_unicode(self):
        """Test detection of Unicode format."""
        self.assertEqual(
            self.service.detect_format("བསྒྲུབས"),
            'unicode'
        )
        self.assertEqual(
            self.service.detect_format("བླ་མ"),
            'unicode'
        )
    
    def test_detect_tz_marker(self):
        """Test TZ as ACIP marker."""
        # TZ is unique to ACIP
        self.assertEqual(
            self.service.detect_format("TZA"),
            'acip'
        )


class TestACIPAutoConvert(unittest.TestCase):
    """Test auto-conversion with format detection."""
    
    def setUp(self):
        self.service = ACIPService()
    
    def test_auto_convert_acip(self):
        """Test auto-convert from ACIP."""
        result = self.service.auto_convert_to_unicode("BSGRUBS")
        self.assertEqual(result, "བསྒྲུབས")
    
    def test_auto_convert_ewts(self):
        """Test auto-convert from EWTS."""
        result = self.service.auto_convert_to_unicode("bsgrubs")
        self.assertEqual(result, "བསྒྲུབས")
    
    def test_auto_convert_unicode(self):
        """Test auto-convert when already Unicode."""
        result = self.service.auto_convert_to_unicode("བསྒྲུབས")
        self.assertEqual(result, "བསྒྲུབས")


class TestACIPEdgeCases(unittest.TestCase):
    """Test ACIP edge cases and special characters."""
    
    def setUp(self):
        self.service = ACIPService()
    
    def test_acip_comments(self):
        """Test ACIP comment removal."""
        converter = ACIPConverter()
        # @... comments should be removed
        result = converter.acip_to_ewts("KA@001A BA")
        self.assertNotIn("@", result)
        self.assertIn("ka", result.lower())
        self.assertIn("ba", result.lower())
        
        # [...] comments should be removed
        result = converter.acip_to_ewts("KA[ABC]BA")
        self.assertNotIn("[", result)
        self.assertNotIn("]", result)
    
    def test_acip_parentheses(self):
        """Test ACIP parentheses (yichung markers)."""
        converter = ACIPConverter()
        # Regular parentheses are removed
        result = converter.acip_to_ewts("KA(BA)CA")
        self.assertNotIn("(", result)
        self.assertNotIn(")", result)
        
        # /.../ becomes (...)
        result = converter.acip_to_ewts("KA/BA/CA")
        self.assertIn("(", result)
        self.assertIn(")", result)
    
    def test_empty_string(self):
        """Test empty string handling."""
        self.assertEqual(
            self.service.acip_to_unicode(""),
            ""
        )
        self.assertEqual(
            self.service.unicode_to_acip(""),
            ""
        )


class TestACIPRoundtrip(unittest.TestCase):
    """Test roundtrip conversion (ACIP → Unicode → ACIP)."""
    
    def setUp(self):
        self.service = ACIPService()
    
    def test_roundtrip_simple(self):
        """Test simple roundtrip conversion."""
        original = "BSGRUBS"
        unicode_result = self.service.acip_to_unicode(original)
        acip_result = self.service.unicode_to_acip(unicode_result)
        self.assertEqual(acip_result, original)
    
    def test_roundtrip_with_vowel(self):
        """Test roundtrip with vowel."""
        # Use a simpler example for roundtrip test
        original = "KI"
        unicode_result = self.service.acip_to_unicode(original)
        acip_result = self.service.unicode_to_acip(unicode_result)
        self.assertEqual(acip_result, original)
    
    def test_roundtrip_complex(self):
        """Test roundtrip with complex text."""
        original = "SANGS RGYAS"
        unicode_result = self.service.acip_to_unicode(original)
        acip_result = self.service.unicode_to_acip(unicode_result)
        self.assertEqual(acip_result, original)


def suite():
    """Create test suite."""
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestACIPToEWTS))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestEWTSToACIP))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestACIPToUnicode))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUnicodeToACIP))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestACIPBatchOperations))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestACIPFormatDetection))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestACIPAutoConvert))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestACIPEdgeCases))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestACIPRoundtrip))
    
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())

