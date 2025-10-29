#!/usr/bin/env python3
"""
Command Line Interface for Wylie Transliterator
Provides both interactive and file-based transliteration.
"""

import sys
import argparse
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent))

from wylie_transliterator.application.transliteration_service import TransliterationService
from wylie_transliterator.infrastructure.file_processor import FileProcessor


def main_interactive():
    """Interactive mode for command-line transliteration"""
    service = TransliterationService()
    
    if len(sys.argv) > 1:
        # Process command-line arguments
        wylie_input = ' '.join(sys.argv[1:])
        tibetan = service.transliterate_wylie_to_tibetan(wylie_input)
        print(tibetan)
    else:
        # Interactive mode
        print("Extended Wylie Transliterator")
        print("Enter Wylie text (Ctrl+D to exit):")
        print()
        
        try:
            for line in sys.stdin:
                line = line.strip()
                if line:
                    tibetan = service.transliterate_wylie_to_tibetan(line)
                    print(f"Wylie:   {line}")
                    print(f"Tibetan: {tibetan}")
                    print()
        except KeyboardInterrupt:
            print("\nExiting...")


def main_file_processor():
    """File-based transliteration CLI"""
    parser = argparse.ArgumentParser(
        description='Wylie Transliterator - Convert between Wylie and Tibetan Unicode',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input=source.txt --output=result.txt
  %(prog)s --input=wylie.txt --output=tibetan.txt --mode=t
  %(prog)s --input=tibetan.txt --output=wylie.txt --mode=w

Modes:
  t      Wylie to Tibetan Unicode (default)
  w      Tibetan Unicode to Wylie (not yet implemented)
  auto   Auto-detect source format (default)
        """
    )
    
    parser.add_argument(
        '--input',
        required=True,
        help='Input file path'
    )
    
    parser.add_argument(
        '--output',
        required=True,
        help='Output file path'
    )
    
    parser.add_argument(
        '--mode',
        choices=['t', 'w', 'auto'],
        default='auto',
        help='Transliteration mode (default: auto)'
    )
    
    args = parser.parse_args()
    
    # Process the file
    service = TransliterationService()
    processor = FileProcessor(service)
    
    try:
        # Auto-detect and report
        if args.mode == 'auto':
            with open(args.input, 'r', encoding='utf-8') as f:
                sample = f.read(500)
            detected_mode = processor._detect_mode(sample)
            mode_name = "Wylie → Tibetan" if detected_mode == 't' else "Tibetan → Wylie"
            print(f"Auto-detected mode: {mode_name}")
        else:
            mode_name = "Wylie → Tibetan" if args.mode == 't' else "Tibetan → Wylie"
        
        print(f"Transliterating: {mode_name}")
        
        stats = processor.process_file(args.input, args.output, args.mode)
        
        print(f"Processed {stats.input_lines} lines")
        print(f"Input:  {stats.input_chars} characters")
        print(f"Output: {stats.output_chars} characters")
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except NotImplementedError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    # Check if being called as file processor (has --input argument)
    if '--input' in sys.argv:
        main_file_processor()
    else:
        main_interactive()

