"""
Comparison tests: python-wylie-transliteration vs pyewts (ACIP Features)

Tests ACIP conversion to ensure compatibility with pyewts.
"""

import unittest
import sys
import os

# Add pyewts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../pyewts'))

try:
    import pyewts
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../pyewts'))
    import ACIP
    PYEWTS_AVAILABLE = True
except ImportError:
    PYEWTS_AVAILABLE = False

from wylie_transliterator import ACIPService


@unittest.skipUnless(PYEWTS_AVAILABLE, "pyewts not available for comparison")
class TestPyewtsComparisonACIP(unittest.TestCase):
    """Compare ACIP features with pyewts"""
    
    def setUp(self):
        self.pyewts = pyewts.pyewts()
        self.acip_service = ACIPService()
    
    def _compare_acip_to_unicode(self, acip_input):
        """Helper to compare ACIP → Unicode outputs"""
        # pyewts path: ACIP → EWTS → Unicode
        ewts = ACIP.ACIPtoEWTS(acip_input)
        expected = self.pyewts.toUnicode(ewts)
        
        # python-wylie path: ACIP → Unicode
        result = self.acip_service.acip_to_unicode(acip_input)
        
        self.assertEqual(result, expected, 
                        f"\nACIP: {acip_input}\nExpected: {expected}\nGot: {result}")
    
    def _compare_acip_to_ewts(self, acip_input):
        """Helper to compare ACIP → EWTS conversion"""
        expected = ACIP.ACIPtoEWTS(acip_input)
        result = self.acip_service.acip_to_wylie(acip_input)
        
        self.assertEqual(result, expected,
                        f"\nACIP: {acip_input}\nExpected EWTS: {expected}\nGot: {result}")
    
    # === BASIC ACIP ===
    
    def test_simple_acip_words(self):
        """Test simple ACIP words"""
        test_cases = [
            'KA',         # ཀ
            'KHA',        # ཁ
            'GA',         # ག
            'NGA',        # ང
            'BKRA SHIS',  # བཀྲ་ཤིས
        ]
        
        for acip in test_cases:
            with self.subTest(acip=acip):
                self._compare_acip_to_unicode(acip)
    
    def test_acip_vowels(self):
        """Test ACIP vowels"""
        test_cases = [
            'KA',   # ཀ (inherent a)
            'KI',   # ཀི
            'KU',   # ཀུ
            'KE',   # ཀེ
            'KO',   # ཀོ
        ]
        
        for acip in test_cases:
            with self.subTest(acip=acip):
                self._compare_acip_to_unicode(acip)
    
    def test_acip_diphthongs(self):
        """Test ACIP diphthongs (EE, OO)"""
        test_cases = [
            'KEE',  # ཀཻ (ai)
            'KOO',  # ཀཽ (au)
        ]
        
        for acip in test_cases:
            with self.subTest(acip=acip):
                self._compare_acip_to_unicode(acip)
    
    # === ACIP COMPLEX STACKS ===
    
    def test_acip_complex_stacks(self):
        """Test ACIP complex consonant stacks"""
        test_cases = [
            'BSGRUBS',      # བསྒྲུབས
            'BKRA',         # བཀྲ
            'DKON',         # དཀོན
            'MCHOG',        # མཆོག
            'SPYAN',        # སྤྱན
        ]
        
        for acip in test_cases:
            with self.subTest(acip=acip):
                self._compare_acip_to_unicode(acip)
    
    # === ACIP GENITIVE ===
    
    def test_acip_genitive_particles(self):
        """Test ACIP genitive particles"""
        test_cases = [
            "BA'I",    # བའི
            "KA'I",    # ཀའི
            "PA'O",    # པའོ
        ]
        
        for acip in test_cases:
            with self.subTest(acip=acip):
                self._compare_acip_to_unicode(acip)
    
    # === ACIP TS/TZ DISTINCTION ===
    
    def test_acip_ts_tsh_distinction(self):
        """Test ACIP TS (tsh) vs TZ (ts) distinction"""
        test_cases = [
            ('TS', 'tsh'),  # ACIP TS = EWTS tsh = ཚ
            ('TZ', 'ts'),   # ACIP TZ = EWTS ts = ཙ
        ]
        
        for acip_input, expected_ewts in test_cases:
            with self.subTest(acip=acip_input):
                result_ewts = self.acip_service.acip_to_wylie(acip_input)
                self.assertEqual(result_ewts, expected_ewts,
                               f"ACIP {acip_input} should convert to EWTS {expected_ewts}")
                self._compare_acip_to_unicode(acip_input)
    
    # === ACIP CASE HANDLING ===
    
    def test_acip_case_mapping(self):
        """Test ACIP uppercase ↔ EWTS lowercase"""
        test_cases = [
            ('BSGRUBS', 'bsgrubs'),
            ('SANGS RGYAS', 'sangs rgyas'),
        ]
        
        for acip_input, expected_ewts in test_cases:
            with self.subTest(acip=acip_input):
                result_ewts = self.acip_service.acip_to_wylie(acip_input)
                self.assertEqual(result_ewts, expected_ewts,
                               f"ACIP {acip_input} should convert to EWTS {expected_ewts}")
    
    # === ACIP MANTRAS ===
    
    def test_acip_mantras(self):
        """Test ACIP mantras"""
        test_cases = [
            'OM MA NI PA DME HUM',     # ཨོམ་མ་ནི་པ་དམེ་ཧུམ
            'OM',                       # ཨོམ
        ]
        
        for acip in test_cases:
            with self.subTest(acip=acip):
                self._compare_acip_to_unicode(acip)
    
    # === ACIP TO EWTS CONVERSION ===
    
    def test_acip_to_ewts_basic(self):
        """Test ACIP to EWTS conversion"""
        test_cases = [
            'BKRA SHIS',
            'DKON MCHOG',
            'BSGRUBS',
        ]
        
        for acip in test_cases:
            with self.subTest(acip=acip):
                self._compare_acip_to_ewts(acip)
    
    # === ACIP ROUNDTRIP ===
    
    def test_acip_roundtrip_normalized(self):
        """Test ACIP roundtrip produces normalized form"""
        # Note: Roundtrip may normalize to canonical forms
        # E.g., OM → ཨོམ → AOM (explicit form)
        test_cases = [
            ('OM', 'AOM'),           # Vowel-initial normalizes
            ('BKRA', 'BKRA'),        # Regular word stays same
            ('BA\'I', 'BA\'I'),      # Genitive stays same
        ]
        
        for acip_input, expected_roundtrip in test_cases:
            with self.subTest(acip=acip_input):
                # Forward: ACIP → Unicode
                unicode_result = self.acip_service.acip_to_unicode(acip_input)
                
                # Backward: Unicode → ACIP
                roundtrip = self.acip_service.unicode_to_acip(unicode_result)
                
                self.assertEqual(roundtrip, expected_roundtrip,
                               f"Roundtrip: {acip_input} → {unicode_result} → {roundtrip}")
    
    # === ACIP LONG TEXT ===
    
    def test_acip_long_text(self):
        """Test longer ACIP text"""
        test_cases = [
            'SANGS RGYAS DANG BYANG CHUB',
            'DKON MCHOG GSUM',
        ]
        
        for acip in test_cases:
            with self.subTest(acip=acip):
                self._compare_acip_to_unicode(acip)


if __name__ == '__main__':
    unittest.main()

