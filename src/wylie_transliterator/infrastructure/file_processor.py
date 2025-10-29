"""
File Processor - Infrastructure Layer
Handles file I/O operations for transliteration.
"""

import re
from pathlib import Path
from typing import Tuple
from ..application.transliteration_service import TransliterationService, TransliterationStatistics


class FileProcessor:
    """Infrastructure service for file-based transliteration"""
    
    def __init__(self, service: TransliterationService):
        self.service = service
    
    def process_file(
        self,
        input_path: str,
        output_path: str,
        mode: str = 'auto'
    ) -> TransliterationStatistics:
        """
        Process a file for transliteration.
        
        Args:
            input_path: Path to input file
            output_path: Path to output file
            mode: 'w' (wylie→tibetan), 't' (tibetan→wylie), or 'auto'
            
        Returns:
            Statistics about the transliteration
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If mode is invalid
        """
        # Read input
        input_text = self._read_file(input_path)
        
        # Auto-detect mode if needed
        if mode == 'auto':
            mode = self._detect_mode(input_text)
        
        # Validate mode
        if mode not in ['t', 'w']:
            raise ValueError(f"Invalid mode: {mode}. Must be 'w', 't', or 'auto'")
        
        # Transliterate
        if mode == 'w':
            # Wylie → Tibetan
            output_text = self.service.transliterate_wylie_to_tibetan(input_text)
        elif mode == 't':
            # Tibetan → Wylie
            output_text = self.service.transliterate_tibetan_to_wylie(input_text)
        
        # Write output
        self._write_file(output_path, output_text)
        
        # Calculate statistics
        stats = TransliterationStatistics(
            input_chars=len(input_text),
            output_chars=len(output_text),
            input_lines=input_text.count('\n') + 1,
            output_lines=output_text.count('\n') + 1
        )
        
        return stats
    
    def _read_file(self, path: str) -> str:
        """Read file with UTF-8 encoding"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {path}")
        except Exception as e:
            raise IOError(f"Error reading file {path}: {e}")
    
    def _write_file(self, path: str, content: str) -> None:
        """Write file with UTF-8 encoding, creating directories if needed"""
        try:
            output_file = Path(path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise IOError(f"Error writing file {path}: {e}")
    
    def _detect_mode(self, text: str) -> str:
        """
        Auto-detect whether text is Wylie or Tibetan Unicode.
        
        Returns:
            'w' for Wylie input (transliterate to Tibetan)
            't' for Tibetan input (transliterate to Wylie)
        """
        # Sample first 500 chars
        sample = text[:500]
        
        # Count Tibetan Unicode characters (U+0F00 to U+0FFF)
        tibetan_chars = len(re.findall(r'[\u0F00-\u0FFF]', sample))
        
        # If more than 30% is Tibetan Unicode, it's Tibetan
        if len(sample) > 0 and tibetan_chars / len(sample) > 0.3:
            return 't'  # Tibetan to Wylie
        
        # Otherwise assume Wylie input
        return 'w'  # Wylie to Tibetan

