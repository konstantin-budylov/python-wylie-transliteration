# Tibetan Wylie Transliterator

A Python implementation of the [THL Extended Wylie Transliteration Scheme (EWTS)](https://texts.mandala.library.virginia.edu/text/thl-extended-wylie-transliteration-scheme) with **bidirectional** conversion and validation.

## Features

✅ **Bidirectional Transliteration**
- **Forward**: Wylie → Tibetan Unicode
- **Reverse**: Tibetan Unicode → Wylie
- Auto-detection of input format
- Batch processing support

✅ **Complete EWTS Implementation**
- 30 basic Tibetan consonants + 12 Sanskrit extensions
- All vowel modifications (a, i, u, e, o, A, U)
- Subscripts (r, l, y, w, m) including double subscripts
- Superscripts (r, l, s)
- Prescripts (g, d, b, m, ') and postscripts
- Tibetan numerals, punctuation, Sanskrit marks
- Smart case normalization for Sanskrit retroflex

✅ **Input Validation** 
- EWTS standard compliance checking
- Detailed error messages with suggestions
- Character validation
- Syllable structure validation
- Stack combination validation
- Position tracking for errors

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

# Forward transliteration (Wylie → Tibetan)
tibetan = service.transliterate_wylie_to_tibetan("bla ma")
print(tibetan)  # བླ་མ

# Reverse transliteration (Tibetan → Wylie)
wylie = service.transliterate_tibetan_to_wylie("བླ་མ")
print(wylie)  # bla ma

# Sanskrit and mantras
mantra = service.transliterate_wylie_to_tibetan("oM ma Ni pa dme hUM|")
print(mantra)  # ཨོཾ་མ་ཎི་པ་དྨེ་ཧཱུྃ།

# Batch processing
texts = ["sangs rgyas", "byang chub", "chos"]
results = service.transliterate_batch(texts)

# Reverse batch processing
tibetan_texts = ["བླ་མ", "སངས་རྒྱས", "བྱང་ཆུབ"]
wylie_results = service.transliterate_tibetan_to_wylie_batch(tibetan_texts)
```

### Validation

```python
from wylie_transliterator.application.validation_service import ValidationService

validator = ValidationService()

# Simple validation
is_valid = validator.is_valid_wylie("bla ma")  # True

# Detailed validation
result = validator.validate_wylie("xyz123")
if not result.is_valid:
    print(result.get_error_summary())
    # ✗ Found 1 error(s):
    #   - [unknown_character] Unknown characters: x, y, z

# Validate before transliteration
if validator.is_valid_wylie("bla ma"):
    result = service.transliterate_wylie_to_tibetan("bla ma")
    print(result)  # བླ་མ
```

### Command Line

```bash
# Interactive mode (with validation)
python -m wylie_transliterator.cli

# Forward transliteration (Wylie → Tibetan)
./wylie.sh --input=wylie.txt --output=tibetan.txt

# Reverse transliteration (Tibetan → Wylie)
./wylie.sh --input=tibetan.txt --output=wylie.txt --mode=t

# Validation only
./wylie.sh --input=wylie.txt --validate

# Auto-detect mode
./wylie.sh --input=source.txt --output=result.txt --mode=auto

# Using Python CLI directly
python -m wylie_transliterator.cli --input=source.txt --output=result.txt --mode=w
python -m wylie_transliterator.cli --input=tibetan.txt --output=wylie.txt --mode=t
python -m wylie_transliterator.cli --input=wylie.txt --validate
```

## Testing

```bash
# Run all test suites
python tests/test_wylie.py           # Forward transliteration (33 tests)
python tests/test_validation.py      # Validation (21 tests)
python tests/test_reverse_transliteration.py  # Reverse (16 tests)

# All tests: 70/70 passing (100%)
```

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

**Reverse Examples:**

| Tibetan | Wylie         |
|---------|---------------|
| བླ་མ    | `bla ma`      |
| སངས་རྒྱས | `sangs rgyas` |
| བསྒྲུབས  | `bsgrubs`     |
| ༡༩༥༩    | `1959`        |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
python tests/test_wylie.py
python tests/test_validation.py
python tests/test_reverse_transliteration.py

# Type checking
mypy src/

# Code formatting
black src/ tests/

# Linting
pylint src/
```

## Command Line Options

### Bash Script (wylie.sh)

```bash
# Forward transliteration (default)
./wylie.sh --input=wylie.txt --output=tibetan.txt

# Reverse transliteration
./wylie.sh --input=tibetan.txt --output=wylie.txt --mode=t

# Validation only
./wylie.sh --input=wylie.txt --validate

# Auto-detect mode
./wylie.sh --input=source.txt --output=result.txt --mode=auto

# Help
./wylie.sh --help
```

**Modes:**
- `w` - Wylie → Tibetan Unicode (default)
- `t` - Tibetan Unicode → Wylie
- `auto` - Auto-detect input format

### Python CLI

```bash
# File processing with mode
python -m wylie_transliterator.cli --input=FILE --output=FILE --mode=MODE

# Validation only
python -m wylie_transliterator.cli --input=FILE --validate

# Interactive mode
python -m wylie_transliterator.cli
```

## Architecture

This project follows **Domain-Driven Design (DDD)** principles:

### Layers

**Domain Layer** (Business Logic)
- `TibetanAlphabet` - Character mappings (value object)
- `ReverseCharacterMappings` - Reverse mappings (value object)
- `WylieToTibetanTransliterator` - Forward transliteration service
- `TibetanToWylieTransliterator` - Reverse transliteration service
- `WylieValidator` - Validation domain service
- `SyllableParser`, `SyllableBuilder`, `CaseNormalizer` - Supporting services

**Application Layer** (Use Cases)
- `TransliterationService` - Main transliteration API
- `ValidationService` - Validation API

**Infrastructure Layer** (External Interfaces)
- `FileProcessor` - File I/O handling
- `CLI` - Command-line interface


## References

- [THL Extended Wylie Transliteration Scheme](https://texts.mandala.library.virginia.edu/text/thl-extended-wylie-transliteration-scheme)
- [Wikipedia: Wylie Transliteration](https://en.wikipedia.org/wiki/Wylie_transliteration)
- [Tibetan Unicode Standard](https://unicode.org/charts/PDF/U0F00.pdf)

## License

MIT License

## Contributing

Contributions welcome! Please ensure:
- All tests pass (70/70)
- Follow DDD architecture
- Add tests for new features
- Update documentation
- Use type hints

---

