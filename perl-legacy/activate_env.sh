#!/bin/bash
# Activation script for Wylie Transliteration environment

echo "========================================="
echo "Activating Wylie Transliteration Environment"
echo "========================================="

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate wylie-transliteration

# Set up Perl local::lib
export PATH="$HOME/perl5/bin:$PATH"
eval $(perl -I ~/perl5/lib/perl5/ -Mlocal::lib)

echo "✓ Conda environment 'wylie-transliteration' activated"
echo "✓ Perl local::lib configured"
echo ""
echo "Perl version: $(perl --version | grep 'This is perl')"
echo "Python version: $(python --version)"
echo ""
echo "PERL5LIB: $PERL5LIB"
echo ""
echo "Ready to work! Current directory: $(pwd)"
echo "========================================="

