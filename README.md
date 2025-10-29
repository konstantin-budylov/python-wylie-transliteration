# Wylie Transliterator

A Python implementation of the [THL Extended Wylie Transliteration Scheme (EWTS)](https://texts.mandala.library.virginia.edu/text/thl-extended-wylie-transliteration-scheme) for converting Wylie transliteration to Tibetan Unicode script.

## Features

✅ **Complete EWTS Implementation**
- 30 basic Tibetan consonants + 12 Sanskrit extensions
- All vowel modifications (a, i, u, e, o, A)
- Subscripts (r, l, y, w) including double subscripts
- Superscripts (r, l, s)
- Prescripts and postscripts
- Tibetan numerals, punctuation, Sanskrit marks
- Smart case normalization

✅ **Input Validation**
- EWTS standard compliance checking
- Detailed error messages with suggestions
- Character validation
- Syllable structure validation
- Stack combination validation



## Quick Start

### Installation

```bash
# Install in development mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

### Basic Usage

```python
from wylie_transliterator import TransliterationService

service = TransliterationService()

# Simple transliteration
tibetan = service.transliterate_wylie_to_tibetan("bla ma")
print(tibetan)  # བླ་མ

# Sanskrit and mantras (with proper syllable breaks)
mantra = service.transliterate_wylie_to_tibetan("oM ma Ni pa dme hUM|")
print(mantra)  # ཨོཾ་མ་ཎི་པ་དྨེ་ཧཱུྃ།

# Batch processing
texts = ["sangs rgyas", "byang chub", "chos"]
results = service.transliterate_batch(texts)

# Validation (new!)
from wylie_transliterator.application.validation_service import ValidationService
validator = ValidationService()

# Validate before transliteration
if validator.is_valid_wylie("bla ma"):
    result = service.transliterate_wylie_to_tibetan("bla ma")
    print(result)  # བླ་མ

# Get detailed validation errors
result = validator.validate_wylie("xyz123")
if not result.is_valid:
    print(result.get_error_summary())
    # ✗ Found 1 error(s):
    #   - [unknown_character] Unknown characters: x
```

### Command Line

```bash
# Interactive mode
python -m wylie_transliterator.cli
# or
wylie "bla ma"

# File processing
./wylie.sh --input=source.txt --output=result.txt
# or
python -m wylie_transliterator.cli --input=source.txt --output=result.txt --mode=t
```

## Testing

```bash
# Run all tests
python tests/test_wylie.py

# Expected: 32/32 tests passing (100%)
```

### Test Coverage

- ✅ Basic consonants (30 letters)
- ✅ Sanskrit extensions (12 letters)
- ✅ Vowel modifications
- ✅ Subscripts (including double subscripts)
- ✅ Superscripts
- ✅ Prescripts
- ✅ Postscripts
- ✅ Complex stacks (bsgrubs, etc.)
- ✅ Numerals and punctuation
- ✅ Sanskrit marks
- ✅ Case normalization
- ✅ THL EWTS compliance

## Examples

| Wylie                  | Tibetan | Meaning               |
|------------------------|---------|-----------------------|
| `bla ma`               | བླ་མ    | Guru, teacher         |
| `sangs rgyas`          | སངས་རྒྱས | Buddha                |
| `byang chub`           | བྱང་ཆུབ | Enlightenment         |
| `bsgrubs`              | བསྒྲུབས | Accomplished          |
| `dza sha`              | ཛ་ཤ     | Multi-char consonants |
| `grwa drwa`            | གྲྭ་དྲྭ | Double subscripts     |
| `1959`                 | ༡༩༥༩    | Tibetan numerals      |
| `oM ma Ni pa dme hUM\|` | ཨོཾ་མ་ཎི་པ་དྨེ་ཧཱུྃ། | Om Mani Padme Hum (mantra) |


## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
python tests/test_wylie.py

# Type checking
mypy src/

# Code formatting
black src/ tests/

# Linting
pylint src/
```

## References

- [THL Extended Wylie Transliteration Scheme](https://texts.mandala.library.virginia.edu/text/thl-extended-wylie-transliteration-scheme)
- [Wikipedia: Wylie Transliteration](https://en.wikipedia.org/wiki/Wylie_transliteration)

## License

MIT License

## Contributing

Contributions welcome! Please ensure:
- All tests pass
- Follow DDD architecture
- Add tests for new features
- Update documentation

---

**Status**: ✅ Production Ready  
**Architecture**: Clean DDD Implementation  
**Tests**: 32/32 passing (100%)  
**Code Quality**: Type-safe, well-documented, SOLID principles
