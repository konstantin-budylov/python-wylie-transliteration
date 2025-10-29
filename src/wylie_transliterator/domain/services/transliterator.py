"""
Wylie to Tibetan Transliterator Domain Service
Coordinates the transliteration process using parser and builder services.
"""

from typing import Tuple
from .syllable_parser import MultiStrategySyllableParser
from .syllable_builder import SyllableBuilder
from .case_normalizer import CaseNormalizer
from ..value_objects.character_mappings import TibetanAlphabet


class WylieToTibetanTransliterator:
    """
    Domain Service for transliterating Wylie to Tibetan Unicode.
    
    This is the core domain service that coordinates:
    - Case normalization
    - Syllable parsing
    - Syllable building
    - Special character handling (numbers, punctuation, Sanskrit)
    """
    
    def __init__(self):
        self.parser = MultiStrategySyllableParser()
        self.builder = SyllableBuilder()
        self.normalizer = CaseNormalizer()
        self.alphabet = TibetanAlphabet()
    
    def transliterate(self, wylie_text: str, spaces_as_tsheg: bool = True) -> str:
        """
        Transliterate Wylie text to Tibetan Unicode.
        
        Args:
            wylie_text: Input in Wylie transliteration
            spaces_as_tsheg: Convert spaces to tsheg (་) if True
            
        Returns:
            Tibetan Unicode string
        """
        # Normalize case
        normalized = self.normalizer.normalize(wylie_text)
        
        # Process character by character
        result = []
        i = 0
        
        while i < len(normalized):
            # Check for numerals
            if normalized[i].isdigit():
                result.append(self.alphabet.NUMERALS.get(normalized[i], normalized[i]))
                i += 1
                continue
            
            # Check for space/tsheg
            if normalized[i] == ' ':
                if spaces_as_tsheg:
                    result.append('\u0F0B')  # tsheg
                else:
                    result.append(' ')
                i += 1
                continue
            
            # Check for punctuation (multi-char first)
            punct_matched, punct_len = self._match_punctuation(normalized[i:])
            if punct_matched:
                result.append(punct_matched)
                i += punct_len
                continue
            
            # Check for Sanskrit marks
            mark_matched, mark_len = self._match_sanskrit_mark(normalized[i:])
            if mark_matched:
                result.append(mark_matched)
                i += mark_len
                continue
            
            # Try to match syllable
            syllable_unicode, syllable_len = self._match_syllable(normalized[i:])
            if syllable_unicode:
                result.append(syllable_unicode)
                i += syllable_len
            else:
                # Pass through unknown character
                result.append(normalized[i])
                i += 1
        
        return ''.join(result)
    
    def _match_punctuation(self, text: str) -> Tuple[str, int]:
        """Match punctuation marks (longest first)"""
        for punct_len in [2, 1]:
            if len(text) >= punct_len:
                punct = text[:punct_len]
                if punct in self.alphabet.PUNCTUATION:
                    return self.alphabet.PUNCTUATION[punct], punct_len
        return '', 0
    
    def _match_sanskrit_mark(self, text: str) -> Tuple[str, int]:
        """Match Sanskrit marks (longest first)"""
        for mark_len in [2, 1]:
            if len(text) >= mark_len:
                mark = text[:mark_len]
                if mark in self.alphabet.SANSKRIT_MARKS:
                    return self.alphabet.SANSKRIT_MARKS[mark], mark_len
        return '', 0
    
    def _match_syllable(self, text: str) -> Tuple[str, int]:
        """
        Match and convert a Wylie syllable to Tibetan.
        
        Returns:
            Tuple of (tibetan_unicode, matched_length)
        """
        components = self.parser.parse_syllable(text)
        
        if not components or not components.root:
            return '', 0
        
        # Calculate matched length
        matched_len = 0
        if components.prescript:
            matched_len += len(components.prescript)
        if components.superscript:
            matched_len += len(components.superscript)
        matched_len += len(components.root)
        if components.subscript:
            # Handle double subscripts
            if '+' in components.subscript:
                matched_len += sum(len(s) for s in components.subscript.split('+'))
            else:
                matched_len += len(components.subscript)
        if components.vowel:
            matched_len += len(components.vowel)
        if components.postscript1:
            matched_len += len(components.postscript1)
        if components.postscript2:
            matched_len += len(components.postscript2)
        
        # Build syllable
        wylie_text = text[:matched_len]
        syllable = self.builder.build_syllable(components, wylie_text)
        
        return syllable.unicode_text, matched_len

