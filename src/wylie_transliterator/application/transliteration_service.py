"""
Transliteration Service - Application Layer
Provides high-level use cases for transliteration operations.
"""

from ..domain.services.transliterator import WylieToTibetanTransliterator
from ..domain.services.tibetan_to_wylie import TibetanToWylieTransliterator


class TransliterationService:
    """
    Application Service coordinating transliteration use cases.
    
    This is the main entry point for application-level operations.
    Domain services are hidden behind this application service.
    
    Supports bidirectional transliteration:
    - Wylie → Tibetan Unicode
    - Tibetan Unicode → Wylie
    """
    
    def __init__(self):
        self._wylie_to_tibetan = WylieToTibetanTransliterator()
        self._tibetan_to_wylie = TibetanToWylieTransliterator()
    
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
        return self._wylie_to_tibetan.transliterate(wylie_text, spaces_as_tsheg)
    
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
    
    def transliterate_tibetan_to_wylie(self, tibetan_text: str) -> str:
        """
        Use Case: Transliterate Tibetan Unicode to Wylie.
        
        Args:
            tibetan_text: Input text in Tibetan Unicode
            
        Returns:
            Wylie transliteration string
            
        Example:
            >>> service = TransliterationService()
            >>> service.transliterate_tibetan_to_wylie('བླ་མ')
            'bla ma'
        """
        return self._tibetan_to_wylie.transliterate(tibetan_text)
    
    def transliterate_tibetan_to_wylie_batch(self, tibetan_texts: list[str]) -> list[str]:
        """
        Use Case: Transliterate multiple Tibetan texts to Wylie.
        
        Args:
            tibetan_texts: List of Tibetan Unicode texts
            
        Returns:
            List of Wylie transliteration strings
            
        Example:
            >>> service = TransliterationService()
            >>> service.transliterate_tibetan_to_wylie_batch(['བླ་མ', 'སངས་རྒྱས'])
            ['bla ma', 'sangs rgyas']
        """
        return [self.transliterate_tibetan_to_wylie(text) for text in tibetan_texts]


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

