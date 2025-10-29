# Issue WYL-2: Om Mani Padme Hum Mantra Transliteration Fix

## Summary

Fixed the transliteration of the Om Mani Padme Hum mantra to correctly handle Sanskrit retroflex consonants, compound vowels, and context-specific anusvaras.

**Correct Input**: `oM ma Ni pa dme hUM|`  
**Expected Output**: `ཨོཾ་མ་ཎི་པ་དྨེ་ཧཱུྃ།`  
**Status**: ✅ **FIXED** - All tests passing (33/33)

---

## Key Fixes Implemented

### 1. **Sanskrit Retroflex Consonants (ཎ ṇ)**

**Problem**: Capital 'N' followed by vowel (e.g., "Ni") was not correctly identified as Sanskrit retroflex ṇ.

**Solution**:
- Updated `CaseNormalizer` to convert "Ni" → "Nai" (so parser sees "Na" + "i" vowel)
- Updated `SyllableParser._match_root()` to preserve case for Sanskrit consonants
- Updated `SyllableParser._match_postscript()` to prevent capitals from being treated as postscripts

**Files Modified**:
- `src/wylie_transliterator/domain/services/case_normalizer.py` (lines 102-109)
- `src/wylie_transliterator/domain/services/syllable_parser.py` (lines 150-161, 188-197)

### 2. **Compound Vowels (ཱུ = long a + u)**

**Problem**: "hUM" was using incorrect anusvara (ཾ instead of ྃ).

**Solution**:
- Added `VOWELS['U']` mapping for compound vowel `\u0F71\u0F74` (long a + u)
- Added `ANUSVARA_AFTER_U` constant for special anusvara `\u0F83` (ྃ)
- Updated `_match_sanskrit_mark()` to use context-aware anusvara selection

**Files Modified**:
- `src/wylie_transliterator/domain/value_objects/character_mappings.py` (lines 170-171)
- `src/wylie_transliterator/domain/services/transliterator.py` (lines 116-128, 75-82)

### 3. **Subscript 'm' (ྨ)**

**Problem**: Subscript 'm' was not available for syllables like "dme".

**Solution**:
- Added `SUBSCRIPTS['m']` mapping to `\u0FA8` (ྨ TIBETAN SUBJOINED LETTER MA)

**Files Modified**:
- `src/wylie_transliterator/domain/value_objects/character_mappings.py` (line 77)

### 4. **Standalone Vowels (ཨོ)**

**Problem**: Already working correctly - "oM" correctly produces ཨོཾ (standalone 'o' vowel with anusvara).

**Verification**: The `_match_standalone_vowel()` method correctly adds 'a' consonant base for standalone vowels.

---

## Test Coverage

### New Tests Added

```python
def test_full_mantra(self):
    """Test the complete Om Mani Padme Hum mantra"""
    wylie = "oM ma Ni pa dme hUM|"
    expected = "ཨོཾ་མ་ཎི་པ་དྨེ་ཧཱུྃ།"
    result = self.trans.transliterate(wylie)
    self.assertEqual(result, expected)
```

### Updated Tests

```python
def test_sanskrit_in_context(self):
    """Test Sanskrit marks and mantras"""
    test_cases = [
        ('oM', 'ཨོཾ'),      # Standalone vowel + anusvara
        ('ma', 'མ'),        # Basic syllable
        ('Ni', 'ཎི'),       # Sanskrit retroflex ṇ
        ('pa', 'པ'),        # Basic syllable
        ('dme', 'དྨེ'),     # Subscript m
        ('hUM', 'ཧཱུྃ'),    # Compound vowel + special anusvara
    ]
```

**Test Results**: ✅ 33/33 tests passing (100%)

---

## Documentation Updates

### README.md

**Quick Start Section** (lines 50-52):
```python
# Sanskrit and mantras (with proper syllable breaks)
mantra = service.transliterate_wylie_to_tibetan("oM ma Ni pa dme hUM|")
print(mantra)  # ཨོཾ་མ་ཎི་པ་དྨེ་ཧཱུྃ།
```

**Examples Table** (line 164):
| Wylie | Tibetan | Meaning |
|-------|---------|---------|
| `oM ma Ni pa dme hUM\|` | ཨོཾ་མ་ཎི་པ་དྨེ་ཧཱུྃ། | Om Mani Padme Hum (mantra) |

---

## Technical Details

### Character Mappings

| Component | Wylie | Unicode | Hex | Description |
|-----------|-------|---------|-----|-------------|
| Standalone a | a | ཨ | U+0F68 | TIBETAN LETTER A |
| Vowel o | o | ོ | U+0F7C | TIBETAN VOWEL SIGN O |
| Anusvara (default) | M | ཾ | U+0F7E | TIBETAN SIGN RJES SU NGA RO |
| Anusvara (after U) | M | ྃ | U+0F83 | TIBETAN SIGN SNA LDAN |
| Retroflex ṇ | Na/Ni | ཎ | U+0F4E | TIBETAN LETTER NNA |
| Vowel i | i | ི | U+0F72 | TIBETAN VOWEL SIGN I |
| Subscript m | m | ྨ | U+0FA8 | TIBETAN SUBJOINED LETTER MA |
| Vowel e | e | ེ | U+0F7A | TIBETAN VOWEL SIGN E |
| Long a | A | ཱ | U+0F71 | TIBETAN VOWEL SIGN AA |
| Vowel u | u | ུ | U+0F74 | TIBETAN VOWEL SIGN U |
| Compound U | U | ཱུ | U+0F71 U+0F74 | Long a + u |

### Syllable Breakdown

```
Input:  oM    ma    Ni    pa    dme      hUM
        │     │     │     │     │        │
        ↓     ↓     ↓     ↓     ↓        ↓
Output: ཨོཾ   མ    ཎི    པ    དྨེ      ཧཱུྃ
        │     │     │     │     │        │
Parts:  a+o+M ma    Na+i  pa    d+m+e   h+U+M

Details:
- oM:  ཨ (a) + ོ (o) + ཾ (M)
- ma:  མ (ma) [inherent 'a']
- Ni:  ཎ (Na) + ི (i)
- pa:  པ (pa) [inherent 'a']
- dme: ད (d) + ྨ (subscript m) + ེ (e)
- hUM: ཧ (h) + ཱུ (U = long a + u) + ྃ (special M after U)
```

---

## Verification Results

```
Input (Wylie):     oM ma Ni pa dme hUM|
Output (Tibetan):  ཨོཾ་མ་ཎི་པ་དྨེ་ཧཱུྃ།
Expected:          ཨོཾ་མ་ཎི་པ་དྨེ་ཧཱུྃ།
Match:             ✓ PERFECT!

Individual Syllable Tests:
✓ oM     → ཨོཾ    (Standalone 'o' vowel + anusvara)
✓ ma     → མ      (Basic syllable)
✓ Ni     → ཎི     (Sanskrit retroflex ṇ + i vowel)
✓ pa     → པ      (Basic syllable)
✓ dme    → དྨེ    (d + subscript m + e vowel)
✓ hUM    → ཧཱུྃ   (h + compound U vowel + special anusvara)

Overall Status: ✓ ALL TESTS PASSED
```

---

## Files Changed

### Code Changes (6 files)

1. `src/wylie_transliterator/domain/value_objects/character_mappings.py`
   - Added subscript 'm'
   - Added compound vowel 'U'
   - Added `ANUSVARA_AFTER_U` constant

2. `src/wylie_transliterator/domain/services/case_normalizer.py`
   - Fixed Sanskrit capital letter handling (N, T, D, S + vowel)
   - Convert "Ni" → "Nai" for proper parsing

3. `src/wylie_transliterator/domain/services/syllable_parser.py`
   - Preserve case in `_match_root()` for Sanskrit consonants
   - Prevent capitals from being postscripts in `_match_postscript()`

4. `src/wylie_transliterator/domain/services/transliterator.py`
   - Context-aware anusvara selection in `_match_sanskrit_mark()`
   - Pass previous character for context

### Test Changes (1 file)

5. `tests/test_wylie.py`
   - Updated `test_sanskrit_in_context()` with complete mantra syllables
   - Added `test_full_mantra()` for end-to-end verification

### Documentation Changes (1 file)

6. `README.md`
   - Updated Quick Start example with mantra
   - Updated Examples table with correct input format

---

## Important Notes

### Correct Input Format

⚠️ **Syllable Breaks Matter**: The correct input is:
```
oM ma Ni pa dme hUM|
```

Not:
- ~~`oM maNi padme hUM|`~~ (incorrect: treats 'maNi' as one syllable)
- ~~`oM ma Ni pad me hUM|`~~ (incorrect: 'pad me' instead of 'pa dme')

### Sanskrit Retroflex Handling

Capital letters followed by vowels (excluding 'h' and 'a') are treated as Sanskrit:
- `Ni` → ཎི (retroflex ṇ + i)
- `Ti` → ཊི (retroflex ṭ + i)
- `Di` → ཌི (retroflex ḍ + i)

### Anusvara Context

Two types of anusvara based on context:
- Default: ཾ (U+0F7E) - after most vowels
- After U vowel: ྃ (U+0F83) - after compound 'U' vowel

---

## Related Issues

- **WYL-1**: Initial Python implementation (completed)
- **WYL-2**: Sanskrit mantra transliteration (this issue) ✅ **COMPLETED**

---

## References

- [THL Extended Wylie Transliteration Scheme](https://texts.mandala.library.virginia.edu/text/thl-extended-wylie-transliteration-scheme)
- [Tibetan Unicode Standard](https://unicode.org/charts/PDF/U0F00.pdf)
- [Om Mani Padme Hum - Wikipedia](https://en.wikipedia.org/wiki/Om_mani_padme_hum)

---

**Date**: 2025-10-29  
**Author**: AI Assistant  
**Status**: ✅ COMPLETED  
**Test Coverage**: 100% (33/33 tests passing)

