#!/bin/bash
# Wylie Transliterator - Console Frontend
# Bidirectional transliteration with validation
# Usage: wylie.sh --input=/path/to/input.txt --output=/path/to/output.txt --mode=auto

# Default values
INPUT_FILE=""
OUTPUT_FILE=""
MODE="auto"
VALIDATE_ONLY=false
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/src/wylie_transliterator/cli.py"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --input=*)
            INPUT_FILE="${1#*=}"
            shift
            ;;
        --output=*)
            OUTPUT_FILE="${1#*=}"
            shift
            ;;
        --mode=*)
            MODE="${1#*=}"
            shift
            ;;
        --validate)
            VALIDATE_ONLY=true
            shift
            ;;
        -h|--help)
            echo "Wylie Transliterator - Bidirectional with Validation"
            echo ""
            echo "Usage:"
            echo "  $0 --input=FILE --output=FILE [--mode=MODE]"
            echo "  $0 --input=FILE --validate"
            echo ""
            echo "Options:"
            echo "  --input=FILE     Input file path (required)"
            echo "  --output=FILE    Output file path (required for transliteration)"
            echo "  --mode=MODE      Transliteration mode (default: auto)"
            echo "  --validate       Validate Wylie input only (no transliteration)"
            echo ""
            echo "Modes:"
            echo "  w      Wylie to Tibetan Unicode (default)"
            echo "  t      Tibetan Unicode to Wylie"
            echo "  auto   Auto-detect source format (default)"
            echo ""
            echo "Examples:"
            echo "  # Forward transliteration"
            echo "  $0 --input=wylie.txt --output=tibetan.txt"
            echo ""
            echo "  # Reverse transliteration"
            echo "  $0 --input=tibetan.txt --output=wylie.txt --mode=t"
            echo ""
            echo "  # Validation only"
            echo "  $0 --input=wylie.txt --validate"
            echo ""
            echo "  # Auto-detect mode"
            echo "  $0 --input=source.txt --output=result.txt --mode=auto"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}Error: Unknown argument: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Validate required arguments
if [ -z "$INPUT_FILE" ]; then
    echo -e "${RED}Error: --input parameter is required${NC}"
    echo "Use --help for usage information"
    exit 1
fi

# Output file is required only if not validating
if [ -z "$OUTPUT_FILE" ] && [ "$VALIDATE_ONLY" = false ]; then
    echo -e "${RED}Error: --output parameter is required (unless using --validate)${NC}"
    echo "Use --help for usage information"
    exit 1
fi

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${RED}Error: Input file not found: $INPUT_FILE${NC}"
    exit 1
fi

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo -e "${RED}Error: Python CLI script not found: $PYTHON_SCRIPT${NC}"
    exit 1
fi

# Validate mode
case $MODE in
    t|w|auto)
        ;;
    *)
        echo -e "${RED}Error: Invalid mode: $MODE${NC}"
        echo "Valid modes: w (wylie→tibetan), t (tibetan→wylie), auto (detect)"
        exit 1
        ;;
esac

# Display operation info
echo -e "${GREEN}Wylie Transliterator${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Input:  $INPUT_FILE"

if [ "$VALIDATE_ONLY" = true ]; then
    echo "Action: Validation only"
else
    echo "Output: $OUTPUT_FILE"
    echo "Mode:   $MODE"
fi
echo ""

# Run Python CLI script
if [ "$VALIDATE_ONLY" = true ]; then
    python3 "$PYTHON_SCRIPT" --input="$INPUT_FILE" --validate
    EXIT_CODE=$?
else
    python3 "$PYTHON_SCRIPT" --input="$INPUT_FILE" --output="$OUTPUT_FILE" --mode="$MODE"
    EXIT_CODE=$?
fi

# Check result
if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    if [ "$VALIDATE_ONLY" = true ]; then
        echo -e "${GREEN}✓ Validation completed successfully${NC}"
    else
        echo -e "${GREEN}✓ Transliteration completed successfully${NC}"
    fi
    exit 0
else
    echo ""
    if [ "$VALIDATE_ONLY" = true ]; then
        echo -e "${RED}✗ Validation failed with exit code $EXIT_CODE${NC}"
    else
        echo -e "${RED}✗ Transliteration failed with exit code $EXIT_CODE${NC}"
    fi
    exit $EXIT_CODE
fi

