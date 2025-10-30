"""
ACIP Service - Application Layer
Provides high-level use cases for ACIP transliteration operations.
"""

from typing import List
from ..domain.services.acip_converter import ACIPConverter
from .transliteration_service import TransliterationService


class ACIPService:
    """
    Application Service for ACIP transliteration.
    
    ACIP (Asian Classics Input Project) is a widely-used transliteration
    system for Tibetan Buddhist texts. This service provides bidirectional
    conversion between ACIP and Tibetan Unicode.
    
    Conversion Flow:
    - ACIP → EWTS → Tibetan Unicode
    - Tibetan Unicode → EWTS → ACIP
    
    This service coordinates between domain services:
    - ACIPConverter (ACIP ↔ EWTS)
    - TransliterationService (EWTS ↔ Unicode)
    """
    
    def __init__(self):
        self._acip_converter = ACIPConverter()
        self._transliteration_service = TransliterationService()
    
    def acip_to_unicode(
        self,
        acip_text: str,
        preserve_spaces: bool = False
    ) -> str:
        """
        Use Case: Convert ACIP transliteration to Tibetan Unicode.
        
        Args:
            acip_text: Input text in ACIP format
            preserve_spaces: If True, keep spaces as spaces; if False, convert to tsheg
            
        Returns:
            Tibetan Unicode string
            
        Example:
            >>> service = ACIPService()
            >>> service.acip_to_unicode("BSGRUBS")
            'བསྒྲུབས'
            >>> service.acip_to_unicode("BLA MA")
            'བླ་མ'
        """
        # Step 1: Convert ACIP to EWTS
        ewts_text = self._acip_converter.acip_to_ewts(acip_text)
        
        # Step 2: Convert EWTS to Tibetan Unicode
        return self._transliteration_service.transliterate_wylie_to_tibetan(
            ewts_text,
            preserve_spaces=preserve_spaces
        )
    
    def unicode_to_acip(self, tibetan_text: str) -> str:
        """
        Use Case: Convert Tibetan Unicode to ACIP transliteration.
        
        Args:
            tibetan_text: Input text in Tibetan Unicode
            
        Returns:
            ACIP transliteration string
            
        Example:
            >>> service = ACIPService()
            >>> service.unicode_to_acip("བསྒྲུབས")
            'BSGRUBS'
            >>> service.unicode_to_acip("བླ་མ")
            'BLA MA'
        """
        # Step 1: Convert Tibetan Unicode to EWTS
        ewts_text = self._transliteration_service.transliterate_tibetan_to_wylie(
            tibetan_text
        )
        
        # Step 2: Convert EWTS to ACIP
        return self._acip_converter.ewts_to_acip(ewts_text)
    
    def acip_to_wylie(self, acip_text: str) -> str:
        """
        Use Case: Convert ACIP directly to EWTS/Wylie (without Unicode).
        
        Useful for format conversion without roundtrip through Unicode.
        
        Args:
            acip_text: Input text in ACIP format
            
        Returns:
            EWTS/Wylie transliteration string
            
        Example:
            >>> service = ACIPService()
            >>> service.acip_to_wylie("BSGRUBS")
            'bsgrubs'
        """
        return self._acip_converter.acip_to_ewts(acip_text)
    
    def wylie_to_acip(self, wylie_text: str) -> str:
        """
        Use Case: Convert EWTS/Wylie directly to ACIP (without Unicode).
        
        Useful for format conversion without roundtrip through Unicode.
        
        Args:
            wylie_text: Input text in EWTS/Wylie format
            
        Returns:
            ACIP transliteration string
            
        Example:
            >>> service = ACIPService()
            >>> service.wylie_to_acip("bsgrubs")
            'BSGRUBS'
        """
        return self._acip_converter.ewts_to_acip(wylie_text)
    
    def acip_to_unicode_batch(
        self,
        acip_texts: List[str],
        preserve_spaces: bool = False
    ) -> List[str]:
        """
        Use Case: Batch convert multiple ACIP texts to Tibetan Unicode.
        
        Args:
            acip_texts: List of ACIP texts to convert
            preserve_spaces: If True, keep spaces as spaces
            
        Returns:
            List of Tibetan Unicode strings
            
        Example:
            >>> service = ACIPService()
            >>> texts = ["BSGRUBS", "BLA MA", "SANGS RGYAS"]
            >>> results = service.acip_to_unicode_batch(texts)
            >>> for result in results:
            ...     print(result)
            བསྒྲུབས
            བླ་མ
            སངས་རྒྱས
        """
        return [
            self.acip_to_unicode(text, preserve_spaces)
            for text in acip_texts
        ]
    
    def unicode_to_acip_batch(
        self,
        tibetan_texts: List[str]
    ) -> List[str]:
        """
        Use Case: Batch convert multiple Tibetan Unicode texts to ACIP.
        
        Args:
            tibetan_texts: List of Tibetan Unicode texts to convert
            
        Returns:
            List of ACIP transliteration strings
            
        Example:
            >>> service = ACIPService()
            >>> texts = ["བསྒྲུབས", "བླ་མ", "སངས་རྒྱས"]
            >>> results = service.unicode_to_acip_batch(texts)
            >>> for result in results:
            ...     print(result)
            BSGRUBS
            BLA MA
            SANGS RGYAS
        """
        return [
            self.unicode_to_acip(text)
            for text in tibetan_texts
        ]
    
    def detect_format(self, text: str) -> str:
        """
        Use Case: Auto-detect if text is in ACIP or EWTS format.
        
        Heuristics:
        - If mostly uppercase with specific ACIP patterns → ACIP
        - If mostly lowercase → EWTS
        - If contains Tibetan Unicode → Unicode
        
        Args:
            text: Input text to detect
            
        Returns:
            Format name: 'acip', 'ewts', or 'unicode'
            
        Example:
            >>> service = ACIPService()
            >>> service.detect_format("BSGRUBS")
            'acip'
            >>> service.detect_format("bsgrubs")
            'ewts'
            >>> service.detect_format("བསྒྲུབས")
            'unicode'
        """
        # Check for Tibetan Unicode characters
        if any('\u0F00' <= c <= '\u0FFF' for c in text):
            return 'unicode'
        
        # Check for ACIP-specific markers
        # TZ is unique to ACIP (EWTS uses 'ts')
        if 'TZ' in text.upper():
            return 'acip'
        
        # Check case: ACIP uses mostly uppercase
        upper_count = sum(1 for c in text if c.isupper())
        lower_count = sum(1 for c in text if c.islower())
        total_alpha = upper_count + lower_count
        
        if total_alpha > 0:
            upper_ratio = upper_count / total_alpha
            # If more than 70% uppercase, likely ACIP
            if upper_ratio > 0.7:
                return 'acip'
        
        # Default to EWTS
        return 'ewts'
    
    def auto_convert_to_unicode(self, text: str) -> str:
        """
        Use Case: Auto-detect format and convert to Tibetan Unicode.
        
        Args:
            text: Input text in any supported format
            
        Returns:
            Tibetan Unicode string
            
        Example:
            >>> service = ACIPService()
            >>> service.auto_convert_to_unicode("BSGRUBS")
            'བསྒྲུབས'
            >>> service.auto_convert_to_unicode("bsgrubs")
            'བསྒྲུབས'
            >>> service.auto_convert_to_unicode("བསྒྲུབས")
            'བསྒྲུབས'
        """
        format_type = self.detect_format(text)
        
        if format_type == 'unicode':
            return text
        elif format_type == 'acip':
            return self.acip_to_unicode(text)
        else:  # ewts
            return self._transliteration_service.transliterate_wylie_to_tibetan(text)

