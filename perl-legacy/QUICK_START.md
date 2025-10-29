# Quick Start Guide

## Environment Setup Complete! ✓

A complete development environment has been created with:
- **Conda environment**: `wylie-transliteration` 
- **Python**: 3.11.14 (as requested)
- **Perl**: 5.34.1 (project language)
- **20+ Perl modules** installed
- **Build system** configured

## Activate the Environment

```bash
# Navigate to project
cd /Volumes/Projects/DEVELOP/_trash/app-linguabo-wylie-transliteration

# Activate (choose one method)

# Method 1: Use the script
source activate_env.sh

# Method 2: Manual
conda activate wylie-transliteration
export PATH="$HOME/perl5/bin:$PATH"
eval $(perl -I ~/perl5/lib/perl5/ -Mlocal::lib)
```

## Current Status

### ✅ Working
- Conda environment
- All dependencies installed
- Build system configured
- Project builds successfully

### ⚠️ Known Issue
- **Module compatibility bug** prevents execution
- Issue: `methods-invoker` vs `utf8::all` conflict
- This is a historical incompatibility from 2013-era Perl
- Code modification needed to resolve

## Next Steps

Choose one path forward:

### Path 1: Fix the Bug (Recommended for Perl Users)
See `ENVIRONMENT_SETUP.md` → "Possible Solutions" section

### Path 2: Learn About the Code
Read `ANALYSIS_SUMMARY.md` for complete code analysis

### Path 3: Python Integration
Since you requested Python, see `ANALYSIS_SUMMARY.md` → "Python Integration Options"

## Documentation Index

| File | Purpose |
|------|---------|
| `QUICK_START.md` | This file - get started quickly |
| `ENVIRONMENT_SETUP.md` | Technical setup details and issue documentation |
| `ANALYSIS_SUMMARY.md` | Complete code analysis and recommendations |
| `README` | Original project README |
| `Changes` | Version history |

## Quick Test

```bash
# Activate environment first (see above)

# Try building
./Build build
# ✓ Should succeed

# Try testing  
./Build test
# ✗ Will fail with known issue

# Check Perl modules installed
perl -MMoo -e 'print "Moo OK\n"'
# ✓ Should print "Moo OK"
```

## Support

All dependencies are installed in:
- **Perl modules**: `~/perl5/`
- **Conda environment**: `/opt/anaconda3/envs/wylie-transliteration`

## What This Project Does

Transliterates Wylie notation (Latin-script representation of Tibetan) into proper Tibetan Unicode script.

**Example** (will work once bug is fixed):
```bash
echo "bsgrubs" | wylie-transliterate
# Should output: བསགྲུབས (Tibetan script)
```

## Questions?

Check the detailed documentation files or examine the code in:
- `lib/App/Lingua/BO/Wylie/Transliteration.pm` (main module)
- `bin/wylie-transliterate` (executable)

---

**Environment created by**: AI Assistant  
**Date**: October 29, 2025  
**Project**: App::Lingua::BO::Wylie::Transliteration v0.1.0

