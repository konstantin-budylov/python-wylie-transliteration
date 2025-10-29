# Deep Analysis: Perl Wylie Transliteration vs THL Extended Wylie Standard

## Executive Summary

The Perl implementation in this repository implements a **basic Wylie transliteration** system but is **NOT fully compliant** with the [THL Extended Wylie Transliteration Scheme](https://texts.mandala.library.virginia.edu/text/thl-extended-wylie-transliteration-scheme#shanti-texts-67584).

## Comparison Table: Perl Implementation vs THL EWTS

### ✅ What the Perl Code Implements Correctly

| Feature | Perl Implementation | THL EWTS | Status |
|---------|---------------------|----------|--------|
| Basic Consonants | 30 letters (k, kh, g, etc.) | Same | ✅ Complete |
| Vowels | a, i, u, e, o | Same | ✅ Complete |
| Subscripts | r, l, y, w/v | r, l, y, w | ✅ Complete |
| Superscripts | r, s, l | r, s, l | ✅ Complete |
| Prescripts | g, d, b, m, ' | Same | ✅ Complete |
| Postscripts | g, ng, d, n, b, m, r, l, s | Same | ✅ Complete |
| Double postscripts | Supported | Supported | ✅ Complete |
| Subjoined letters | For stacks | For stacks | ✅ Complete |

### ❌ Missing THL EWTS Features

| Feature | THL EWTS | Perl Implementation | Gap |
|---------|----------|---------------------|-----|
| **Sanskrit retroflex** | Ta, Tha, Da, Dha, Na, Sha (capitals) | Not implemented | ❌ Missing |
| **Sanskrit marks** | M (anusvara), H (visarga) | Not implemented | ❌ Missing |
| **Punctuation** | \|, \|\|, /, //, ;, :, !, ?, etc. | Not implemented | ❌ Missing |
| **Tsheg** | Space or explicit tsheg | Not implemented | ❌ Missing |
| **Numerals** | 0-9 | Not implemented | ❌ Missing |
| **Special stacks** | +, ~, explicit markers | Not implemented | ❌ Missing |
| **Astrological signs** | Various symbols | Not implemented | ❌ Missing |
| **Name markers** | @, # for proper names | Not implemented | ❌ Missing |

## Detailed Analysis

### 1. Character Mapping Analysis

#### Consonants (Lines 59-101)
```perl
K => "\N{TIBETAN LETTER KA}"      # ཀ  (U+0F40)
KH => "\N{TIBETAN LETTER KHA}"    # ཁ  (U+0F41)
# ... etc
```

**Analysis**: 
- ✅ All 30 basic consonants correctly mapped
- ✅ Aspir ated forms (kh, gh, etc.) included
- ✅ Sanskrit-specific consonants (TT, TTHA, DD, DDHA, NN) included
- ❌ Missing: Capitalized retroflex forms for Sanskrit (Ta, Tha, Da, Dha, Na, Sha per EWTS)

#### Vowels (Lines 177-183)
```perl
A => "\N{TIBETAN VOWEL SIGN AA}"  # ཱ  (U+0F71)
I => "\N{TIBETAN VOWEL SIGN I}"   # ི  (U+0F72)
U => "\N{TIBETAN VOWEL SIGN U}"   # ུ  (U+0F74)
E => "\N{TIBETAN VOWEL SIGN E}"   # ེ  (U+0F7A)
O => "\N{TIBETAN VOWEL SIGN O}"   # ོ  (U+0F7C)
```

**Analysis**:
- ✅ All 5 vowels correctly implemented
- ✅ Inherent 'a' correctly omitted (line 267)
- Note: Uppercase in Perl code but EWTS uses lowercase (i, u, e, o)

### 2. Syllable Structure Algorithm (Lines 204-237)

The Perl code implements **4 regex alternations** to match different syllable patterns:

```
Pattern 1: script + sub? + vowel + post1? + post2?
Pattern 2: pre? + script + sub? + vowel + post1? + post2?
Pattern 3: super? + script + sub? + vowel + post1? + post2?
Pattern 4: pre? + super? + script + sub? + vowel + post1? + post2?
```

**Analysis**:
- ✅ Correctly handles all 7 positions: prescript, superscript, root, subscript, vowel, post1, post2
- ✅ Uses longest-match-first strategy (line 189)
- ⚠️ Case-insensitive matching (line 192: `ix` flag) - EWTS is case-sensitive!
- ✅ Handles stacks via subjoined letters

**According to [THL EWTS](https://texts.mandala.library.virginia.edu/text/thl-extended-wylie-transliteration-scheme#shanti-texts-67584), syllable structure is**:

```
[prescript] [superscript] ROOT [subscript] [vowel] [postscript1] [postscript2]
```

This matches the Perl implementation.

### 3. Subjoined Letter Logic (Lines 264-265)

```perl
$o .= $self->SCRIPT_SUBJ -> {uc $script}  if defined $script and defined $super;
$o .= $self->SCRIPT      -> {uc $script}  if defined $script and $super eq '';
```

**Analysis**:
- ✅ Correctly uses subjoined forms when superscript is present
- ✅ Uses regular forms when no superscript
- This creates proper stacks like: རྐ (r + ka) = rka

### 4. Missing EWTS Features

#### A. Sanskrit Extensions

Per THL EWTS:
> "For the retroflex characters, they took their closest relative, generally the dentals with one exception, and reversed them. In the proposed system, these retroflex characters are handled in a way similar to the Tibetan method, namely by **capitalization of the corresponding dental**."

The Perl code **does not implement**:
- Ta, Tha, Da, Dha, Na, Sha (retroflex consonants)
- M (anusvara: ཾ U+0F7E)
- H (visarga: ཿ U+0F7F)

#### B. Punctuation

THL EWTS defines extensive punctuation:
- `|` → TIBETAN MARK INTERSYLLABIC TSHEG (་ U+0F0B)
- `||` → TIBETAN MARK SHAD (། U+0F0D)
- `/` → Other marks
- Space → word separator

The Perl code **does not handle punctuation**.

#### C. Special Markers

THL EWTS includes:
- `+` for explicit stacking
- `_` for explicit disambiguation
- `@` for name markers
- Numerals 0-9

The Perl code **does not implement these**.

## Code Quality Assessment

### Strengths
1. **Clean OO Design**: Uses Moo for modern Perl OO
2. **Lazy Loading**: Efficient memory usage
3. **Regex-based**: Fast pattern matching
4. **Unicode Named Characters**: Self-documenting

### Weaknesses
1. **Case Insensitivity**: EWTS is case-sensitive (important for Sanskrit)
2. **Incomplete**: Missing 50%+ of EWTS features
3. **No Error Handling**: Silently fails on invalid input
4. **No Validation**: Accepts invalid Wylie sequences
5. **No Round-trip**: Can't convert Tibetan → Wylie

### Bugs/Issues
1. **Line 265**: `$super eq ''` should be `!defined $super` or `$super // '' eq ''`
2. **Line 267**: Uppercase comparison `uc($vowel) eq 'A'` inconsistent with lowercase EWTS
3. **No word boundary handling**: Processes character-by-character

## THL EWTS Standard Summary

Based on the [THL specification](https://texts.mandala.library.virginia.edu/text/thl-extended-wylie-transliteration-scheme#shanti-texts-67584):

### Core Principles
1. **Case-sensitive**: Capitals for Sanskrit retroflex
2. **ASCII-only**: No diacritics required
3. **Unambiguous**: One-to-one mapping
4. **Comprehensive**: Covers all Tibetan + Sanskrit in Tibetan script

### Character Sets

**Consonants (30):**
```
k kh g ng | c ch j ny | t th d n | p ph b m
ts tsh dz w | zh z ' y | r l sh s h a
```

**Sanskrit Additional (via capitals):**
```
Ta Tha Da Dha Na Sha (retroflex)
M (anusvara), H (visarga)
```

**Vowels:**
```
a (inherent), i, u, e, o
-i, -I (reverse vowels)
```

**Stacks:**
- Subscripts: r, l, y, w
- Superscripts: r, s, l
- Prescripts: g, d, b, m, '

**Punctuation:**
- ` ` (space) → tsheg (word separator)
- `|` → shad (།)
- `||` → double shad
- `/`, `//`, etc.

## Recommendations for Python Implementation

### Must Have (Core Wylie)
1. ✅ All 30 consonants
2. ✅ All 5 vowels
3. ✅ All stacks (prescripts, superscripts, subscripts)
4. ✅ Postscripts
5. ✅ Proper syllable structure

### Should Have (EWTS Extensions)
1. ✅ Sanskrit retroflex (Ta, Tha, Da, Dha, Na, Sha)
2. ✅ Sanskrit marks (M, H)
3. ✅ Punctuation (|, ||, /, etc.)
4. ✅ Tsheg handling
5. ✅ Numerals

### Nice to Have
1. Round-trip conversion (Tibetan → Wylie)
2. Validation and error reporting
3. Support for special markers (+, _, @, #)
4. Astrological signs
5. Canonical stack ordering

## Test Cases Needed

Based on examples from [THL EWTS](https://texts.mandala.library.virginia.edu/text/thl-extended-wylie-transliteration-scheme#shanti-texts-67584):

```
# Basic
bsgrubs → བསྒྲུབས
dbu → དབུ
phywa → ཕྱྭ

# Stacks
rka → རྐ
grwa → གྲྭ
bskyabs → བསྐྱབས

# Sanskrit
TaMa → ཊཾ
DharmaH → དྷརྨཿ

# Complex
skra → སྐྲ  (s + k + r + a)
bsgrubs → བསྒྲུབས (b + s + g + r + u + b + s)
```

## References

1. [THL Extended Wylie Transliteration Scheme](https://texts.mandala.library.virginia.edu/text/thl-extended-wylie-transliteration-scheme#shanti-texts-67584) - Official specification
2. [Wikipedia: Wylie Transliteration](https://en.wikipedia.org/wiki/Wylie_transliteration) - Historical context
3. [Unicode Tibetan Block](https://www.unicode.org/charts/PDF/U0F00.pdf) - U+0F00–U+0FFF
4. Turrell Wylie, "A Standard System of Tibetan Transcription," Harvard Journal of Asiatic Studies, vol. 22 (December 1959), 261-67

## Conclusion

The Perl implementation is a **partial implementation** of basic Wylie transliteration covering approximately **40-50% of the THL Extended Wylie standard**. It handles the core syllable structure well but lacks:
- Sanskrit extensions (critical for Buddhist texts)
- Punctuation (essential for proper text rendering)
- Special markers and numerals
- Validation and error handling

A complete Python implementation should address all these gaps to achieve full EWTS compliance.

