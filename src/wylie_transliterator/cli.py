#!/usr/bin/env python3
"""
Command Line Interface for Wylie Transliterator
Provides transliteration, validation, and file processing.
"""

import sys
import argparse
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent))

from wylie_transliterator.application.transliteration_service import TransliterationService
from wylie_transliterator.application.validation_service import ValidationService
from wylie_transliterator.infrastructure.file_processor import FileProcessor


def main_interactive():
    """Interactive mode for command-line transliteration"""
    service = TransliterationService()
    validator = ValidationService()
    
    if len(sys.argv) > 1:
        # Process command-line arguments
        wylie_input = ' '.join(sys.argv[1:])
        
        # Validate first
        result = validator.validate_wylie(wylie_input)
        if not result.is_valid:
            print(f"⚠️  Warning: {result.get_error_summary()}", file=sys.stderr)
        
        # Transliterate
        tibetan = service.transliterate_wylie_to_tibetan(wylie_input)
        print(tibetan)
    else:
        # Interactive mode
        print("Extended Wylie Transliterator (with validation)")
        print("Enter Wylie text (Ctrl+D to exit):")
        print()
        
        try:
            for line in sys.stdin:
                line = line.strip()
                if line:
                    # Validate
                    result = validator.validate_wylie(line)
                    
                    # Transliterate
                    tibetan = service.transliterate_wylie_to_tibetan(line)
                    
                    print(f"Wylie:   {line}")
                    if not result.is_valid:
                        print(f"⚠️  Warning: {result.errors[0].message}")
                    print(f"Tibetan: {tibetan}")
                    print()
        except KeyboardInterrupt:
            print("\nExiting...")


def main_file_processor():
    """File-based transliteration CLI"""
    parser = argparse.ArgumentParser(
        description='Wylie Transliterator - Bidirectional conversion with validation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Forward transliteration (Wylie → Tibetan)
  %(prog)s --input=wylie.txt --output=tibetan.txt
  %(prog)s --input=wylie.txt --output=tibetan.txt --mode=w
  
  # Reverse transliteration (Tibetan → Wylie)
  %(prog)s --input=tibetan.txt --output=wylie.txt --mode=t
  
  # Validation only
  %(prog)s --input=wylie.txt --validate
  
  # Auto-detect mode
  %(prog)s --input=source.txt --output=result.txt --mode=auto

Modes:
  w      Wylie to Tibetan Unicode (default)
  t      Tibetan Unicode to Wylie
  auto   Auto-detect source format
        """
    )
    
    parser.add_argument(
        '--input',
        required=True,
        help='Input file path'
    )
    
    parser.add_argument(
        '--output',
        help='Output file path (required unless --validate)'
    )
    
    parser.add_argument(
        '--mode',
        choices=['w', 't', 'auto'],
        default='auto',
        help='Transliteration mode: w=Wylie→Tibetan, t=Tibetan→Wylie, auto=detect (default: auto)'
    )
    
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate Wylie input only (no transliteration)'
    )
    
    args = parser.parse_args()
    
    # Validation mode
    if args.validate:
        validate_file(args.input)
        return
    
    # Require output for transliteration
    if not args.output:
        print("Error: --output required for transliteration (or use --validate)", file=sys.stderr)
        sys.exit(1)
    
    # Process the file
    service = TransliterationService()
    processor = FileProcessor(service)
    
    try:
        # Auto-detect and report
        if args.mode == 'auto':
            with open(args.input, 'r', encoding='utf-8') as f:
                sample = f.read(500)
            detected_mode = processor._detect_mode(sample)
            mode_name = "Wylie → Tibetan" if detected_mode == 'w' else "Tibetan → Wylie"
            print(f"Auto-detected mode: {mode_name}")
            actual_mode = detected_mode
        else:
            mode_name = "Wylie → Tibetan" if args.mode == 'w' else "Tibetan → Wylie"
            actual_mode = args.mode
        
        print(f"Transliterating: {mode_name}")
        
        stats = processor.process_file(args.input, args.output, actual_mode)
        
        print(f"✅ Processed {stats.input_lines} lines")
        print(f"   Input:  {stats.input_chars} characters")
        print(f"   Output: {stats.output_chars} characters")
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except NotImplementedError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def validate_file(input_path):
    """Validate a Wylie file and report errors"""
    validator = ValidationService()
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Validating: {input_path}")
        print("="*70)
        
        # Split into lines for better reporting
        lines = content.split('\n')
        total_errors = 0
        total_warnings = 0
        
        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue
            
            result = validator.validate_wylie(line)
            
            if not result.is_valid:
                print(f"\nLine {line_num}: {line[:50]}...")
                for error in result.errors[:3]:  # Show first 3 errors
                    print(f"  ✗ {error.message}")
                total_errors += len(result.errors)
            
            if result.warnings:
                total_warnings += len(result.warnings)
        
        print("\n" + "="*70)
        if total_errors == 0:
            print(f"✅ All valid! (0 errors, {total_warnings} warnings)")
        else:
            print(f"❌ Found {total_errors} error(s), {total_warnings} warning(s)")
            sys.exit(1)
        
    except FileNotFoundError:
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    # Check if being called as file processor (has --input argument)
    if any('--input' in arg for arg in sys.argv):
        main_file_processor()
    else:
        main_interactive()
