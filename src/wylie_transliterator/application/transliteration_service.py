"""
Transliteration Service - Application Layer
Provides high-level use cases for transliteration operations.
"""

from ..domain.services.transliterator import WylieToTibetanTransliterator


class TransliterationService:
    """
    Application Service coordinating transliteration use cases.
    
    This is the main entry point for application-level operations.
    Domain services are hidden behind this application service.
    """
    
    def __init__(self):
        self._transliterator = WylieToTibetanTransliterator()
    
    def transliterate_wylie_to_tibetan(
        self,
        wylie_text: str,
        preserve_spaces: bool = False
    ) -> str:
        """
        Use Case: Transliterate Wylie text to Tibetan Unicode.
        
        Args:
            wylie_text: Input text in Wylie transliteration
            preserve_spaces: If True, keep spaces as spaces; if False, convert to tsheg
            
        Returns:
            Tibetan Unicode string
            
        Example:
            >>> service = TransliterationService()
            >>> service.transliterate_wylie_to_tibetan("bla ma")
            'བླ་མ'
        """
        spaces_as_tsheg = not preserve_spaces
        return self._transliterator.transliterate(wylie_text, spaces_as_tsheg)
    
    def transliterate_batch(
        self,
        wylie_texts: list[str],
        preserve_spaces: bool = False
    ) -> list[str]:
        """
        Use Case: Transliterate multiple Wylie texts.
        
        Args:
            wylie_texts: List of Wylie texts
            preserve_spaces: Whether to preserve spaces
            
        Returns:
            List of Tibetan Unicode strings
        """
        return [
            self.transliterate_wylie_to_tibetan(text, preserve_spaces)
            for text in wylie_texts
        ]


class TransliterationStatistics:
    """Value Object for transliteration statistics"""
    
    def __init__(
        self,
        input_chars: int,
        output_chars: int,
        input_lines: int,
        output_lines: int
    ):
        self.input_chars = input_chars
        self.output_chars = output_chars
        self.input_lines = input_lines
        self.output_lines = output_lines
    
    def __str__(self) -> str:
        return (
            f"Input: {self.input_lines} lines, {self.input_chars} characters\n"
            f"Output: {self.output_lines} lines, {self.output_chars} characters"
        )

