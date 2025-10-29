# Environment Setup and Analysis Report

## Project Overview

**Name:** App::Lingua::BO::Wylie::Transliteration  
**Version:** 0.1.0  
**Language:** Perl (NOT Python)  
**Purpose:** Transliterate Wylie transliteration to Classical Tibetan Unicode script  

## Deep Code Analysis

### Architecture
- Uses Moo (Modern Minimalist Object Orientation for Perl)  
- Implements lazy-loaded hash maps for Tibetan character positions
- Complex regex-based pattern matching with named capture groups
- Handles 7-position Tibetan syllable structure:
  1. Prescript
  2. Superscript
  3. Center piece (mandatory)
  4. Subscript
  5. Vowel sign
  6. Postscript1
  7. Postscript2

### Dependencies
**Runtime:**
- Perl v5.14.0+
- Moo
- MooX::Options
- MooX::Types::MooseLike::Base
- utf8::all
- autovivification
- methods (with invoker)
- true
- FindBin

**Testing:**
- Test::More
- Test::CheckDeps
- Test::UseAllModules

**Build:**
- Module::Build
- ExtUtils::MakeMaker
- Dist::Zilla

## Environment Setup

### Conda Environment Created
```bash
conda create -n wylie-transliteration -c conda-forge python=3.11 perl -y
```

**Contents:**
- Python 3.11.14 (as requested, though project is Perl)
- Perl 5.34.1
- Various system libraries

### Perl Modules Installed (via cpanm to ~/perl5)

**Successfully Installed:**
- local::lib
- App::cpanminus
- Moo
- Role::Tiny
- MooX::Options (with dependencies: Text::LineFold, MooX::Locale::Passthrough, MIME::Charset, Unicode::LineBreak)
- MooX::Types::MooseLike::Base
- utf8::all (with PerlIO::utf8_strict)
- autovivification
- B::OPCheck
- B::Utils
- B::Hooks::OP::Annotation
- B::Hooks::OP::Check
- invoker
- true
- methods
- Method::Signatures::Simple
- namespace::sweep
- Function::Parameters
- Module::Build
- Test::Simple/Test::More
- Test::CheckDeps
- Test::UseAllModules
- Devel::Declare

## Current Issues

### Known Bug: Module Loading Order Conflict
There is a compatibility issue between `methods-invoker` and `utf8::all` modules:

1. **Problem:** The `methods-invoker` pragma (which enables the `method` keyword) conflicts with `utf8::all`'s source filtering
2. **Error:** "Couldn't find declarator 'method'"
3. **Location:** Occurs when parsing method declarations starting at line 37 of Transliteration.pm

### Attempted Solutions
1. Reordering module imports - unsuccessful due to interdependencies
2. Installing local versions of all modules to avoid system conflicts - partially successful
3. Various combinations of module loading order - unsuccessful

### Root Cause
The `utf8::all` module modifies Perl's source code filtering/parsing, which interferes with `Devel::Declare`-based syntax extensions like `methods-invoker`. This is a known incompatibility in older Perl module ecosystems.

## Activation Script

To use the environment:

```bash
# Activate conda environment
conda activate wylie-transliteration

# Set up Perl local::lib
export PATH="$HOME/perl5/bin:$PATH"
eval $(perl -I ~/perl5/lib/perl5/ -Mlocal::lib)

# Navigate to project
cd /Volumes/Projects/DEVELOP/_trash/app-linguabo-wylie-transliteration
```

## Possible Solutions (Not Implemented)

1. **Replace methods-invoker:** Rewrite code to use standard Perl `sub` syntax instead of `method` keyword
2. **Remove utf8::all:** Replace with standard `use utf8;` and explicit encodings
3. **Use Function::Parameters:** Modern replacement for method syntax (requires code refactoring)
4. **Upgrade to Moo + Kavorka:** Modern method signature handling

## Build Commands

```bash
# Configure build
perl Build.PL

# Build project
./Build build

# Run tests (currently fails due to module issue)
./Build test

# If working, install with:
./Build install
```

## Test Example

Once the module loading issue is resolved, the application should work like this:

```bash
# Command line usage
echo "bsgrubs" | wylie-transliterate

# Or with file input  
wylie-transliterate input.txt
```

## Files Modified

- `lib/App/Lingua/BO/Wylie/Transliteration.pm` - Attempted module load order fixes (needs restoration to original or further fixes)

## Recommendations

1. For immediate use: Consider refactoring to remove `methods-invoker` dependency
2. For modern Perl: Upgrade to use `Function::Parameters` or Moo's native method handling
3. Document: This codebase is from 2013-2014 and uses older Perl idioms

## Python Note

While Python 3.11 was installed per your request, this is fundamentally a Perl project. If you need Python integration, you would need to:
1. Create Python bindings/wrappers
2. Use subprocess to call the Perl script
3. Or port the entire transliteration logic to Python

