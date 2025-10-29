#!/bin/bash
# Wylie Transliterator - Console Frontend
# Usage: wylie.sh --input=/path/to/input.txt --output=/path/to/output.txt --mode=auto

# Default values
INPUT_FILE=""
OUTPUT_FILE=""
MODE="auto"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/src/wylie_transliterator/cli.py"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse command line arguments
for arg in "$@"; do
    case $arg in
        --input=*)
            INPUT_FILE="${arg#*=}"
            shift
            ;;
        --output=*)
            OUTPUT_FILE="${arg#*=}"
            shift
            ;;
        --mode=*)
            MODE="${arg#*=}"
            shift
            ;;
        -h|--help)
            echo "Wylie Transliterator - Console Frontend"
            echo ""
            echo "Usage:"
            echo "  $0 --input=FILE --output=FILE [--mode=MODE]"
            echo ""
            echo "Options:"
            echo "  --input=FILE    Input file path (required)"
            echo "  --output=FILE   Output file path (required)"
            echo "  --mode=MODE     Transliteration mode (default: auto)"
            echo ""
            echo "Modes:"
            echo "  t      Wylie to Tibetan Unicode (default)"
            echo "  w      Tibetan Unicode to Wylie (not yet implemented)"
            echo "  auto   Auto-detect source format (default)"
            echo ""
            echo "Examples:"
            echo "  $0 --input=source.txt --output=result.txt"
            echo "  $0 --input=tibetan.txt --output=wylie.txt --mode=w"
            echo "  $0 --input=wylie.txt --output=tibetan.txt --mode=t"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}Error: Unknown argument: $arg${NC}"
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

if [ -z "$OUTPUT_FILE" ]; then
    echo -e "${RED}Error: --output parameter is required${NC}"
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
        echo "Valid modes: t (wylie→tibetan), w (tibetan→wylie), auto (detect)"
        exit 1
        ;;
esac

# Display operation info
echo -e "${GREEN}Wylie Transliterator${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Input:  $INPUT_FILE"
echo "Output: $OUTPUT_FILE"
echo "Mode:   $MODE"
echo ""

# Run Python CLI script
python3 "$PYTHON_SCRIPT" --input="$INPUT_FILE" --output="$OUTPUT_FILE" --mode="$MODE"
EXIT_CODE=$?

# Check result
if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Transliteration completed successfully${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}✗ Transliteration failed with exit code $EXIT_CODE${NC}"
    exit $EXIT_CODE
fi

