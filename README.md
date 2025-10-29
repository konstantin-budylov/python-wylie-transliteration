# Wylie Transliterator

A production-ready Python implementation of the [THL Extended Wylie Transliteration Scheme (EWTS)](https://texts.mandala.library.virginia.edu/text/thl-extended-wylie-transliteration-scheme) for converting Wylie transliteration to Tibetan Unicode script.

**Architecture**: Domain-Driven Design (DDD)  
**Test Coverage**: 100% (32/32 tests passing)  
**Status**: ✅ Production Ready

## Features

✅ **Complete EWTS Implementation**
- 30 basic Tibetan consonants + 12 Sanskrit extensions
- All vowel modifications (a, i, u, e, o, A)
- Subscripts (r, l, y, w) including double subscripts
- Superscripts (r, l, s)
- Prescripts and postscripts
- Tibetan numerals, punctuation, Sanskrit marks
- Smart case normalization

✅ **Clean Architecture**
- Domain-Driven Design (DDD)
- Separation of Concerns
- SOLID Principles
- Comprehensive test suite
- Type hints throughout

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

## Project Structure

```
wylie-transliterator/
├── src/wylie_transliterator/       # Source code
│   ├── domain/                     # Domain layer (business logic)
│   │   ├── models/                 # Domain entities
│   │   │   └── syllable.py         # Syllable entity & value objects
│   │   ├── services/               # Domain services
│   │   │   ├── syllable_parser.py  # Multi-strategy parser
│   │   │   ├── syllable_builder.py # Unicode builder
│   │   │   ├── case_normalizer.py  # Case normalization
│   │   │   └── transliterator.py   # Main transliterator
│   │   └── value_objects/          # Value objects
│   │       └── character_mappings.py # Tibetan alphabet mappings
│   ├── application/                # Application layer (use cases)
│   │   └── transliteration_service.py # Main service
│   ├── infrastructure/             # Infrastructure layer
│   │   └── file_processor.py       # File I/O
│   └── cli.py                      # CLI interface
├── tests/                          # Test suite
│   ├── test_wylie.py               # 32 comprehensive tests
│   └── test_data/                  # Test data files
├── docs/                           # Documentation
├── perl-legacy/                    # Original Perl implementation
├── setup.py                        # Package configuration
├── wylie.sh                        # Bash frontend
└── README.md                       # This file
```

## Architecture

### Domain-Driven Design Layers

**Domain Layer** (Core Business Logic)
- `Syllable`: Entity representing Tibetan syllable
- `SyllableComponents`: Value object for syllable structure
- `TibetanAlphabet`: Value object for character mappings
- `MultiStrategySyllableParser`: Parsing domain service
- `SyllableBuilder`: Building domain service
- `CaseNormalizer`: Normalization domain service
- `WylieToTibetanTransliterator`: Coordinating domain service

**Application Layer** (Use Cases)
- `TransliterationService`: Main application service
- `TransliterationStatistics`: Statistics value object

**Infrastructure Layer** (External Interfaces)
- `FileProcessor`: File I/O handling
- `CLI`: Command-line interface

### Design Patterns Used

- **Strategy Pattern**: Multi-strategy syllable parsing
- **Builder Pattern**: Syllable construction
- **Service Layer**: Clear separation of concerns
- **Dependency Injection**: Loose coupling between layers
- **Value Objects**: Immutable data structures
- **Repository Pattern**: (Future: for storing translations)

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

## Documentation

- [Architecture Guide](docs/ARCHITECTURE.md) - Detailed DDD architecture
- [Development History](docs/COMPLETION_REPORT.md) - From 44% to 100% tests
- [Perl Analysis](docs/PERL_CODE_ANALYSIS.md) - Original implementation study
- [API Reference](docs/API.md) - Complete API documentation

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

## Version

**Current Version**: 2.0.0
- Complete DDD refactoring
- 100% test coverage
- Production-ready architecture

**Previous Version**: 1.0.0
- Initial implementation
- 44% → 100% test progression

## References

- [THL Extended Wylie Transliteration Scheme](https://texts.mandala.library.virginia.edu/text/thl-extended-wylie-transliteration-scheme)
- [Wikipedia: Wylie Transliteration](https://en.wikipedia.org/wiki/Wylie_transliteration)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)

## License

MIT License - See perl-legacy/LICENSE

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
