"""
Case Normalizer Domain Service
Handles intelligent case normalization for Wylie input.
"""

from ..value_objects.character_mappings import TibetanAlphabet, SyllableRules


class CaseNormalizer:
    """
    Domain Service for normalizing case in Wylie input.
    
    Preserves:
    - Vowel case (A is long vowel, a is inherent)
    - Sanskrit retroflex capitals (Ta, Tha, Da, Dha, Na, Sha)
    - Sanskrit marks (M, H)
    
    Normalizes:
    - Basic consonants (Ka -> ka, KHA -> kha)
    - All-caps input (KA -> ka)
    """
    
    SANSKRIT_RETROFLEX_3 = ['Tha', 'Dha', 'Sha']
    SANSKRIT_RETROFLEX_2 = ['Ta', 'Da', 'Na']
    SANSKRIT_MARKS = ['M', 'H']
    TERMINATOR_CHARS = [' ', '/', '|', '\n', '\t', 'M']  # M can follow sanskrit
    
    def __init__(self):
        self.alphabet = TibetanAlphabet()
    
    def normalize(self, text: str) -> str:
        """
        Normalize case while preserving semantic distinctions.
        
        Args:
            text: Raw Wylie input
            
        Returns:
            Case-normalized Wylie text
        """
        result = []
        i = 0
        
        while i < len(text):
            # Check for Sanskrit retroflex (3-char first)
            matched = False
            for retro in self.SANSKRIT_RETROFLEX_3:
                if text[i:i+len(retro)] == retro:
                    result.append(retro)
                    i += len(retro)
                    matched = True
                    break
            
            if matched:
                continue
            
            # Check for 2-char retroflex (preserve Sanskrit capitals)
            for retro in self.SANSKRIT_RETROFLEX_2:
                if text[i:i+len(retro)] == retro:
                    # Always preserve Sanskrit retroflex
                    result.append(retro)
                    i += len(retro)
                    matched = True
                    break
            
            if matched:
                continue
            
            # Check for standalone Sanskrit marks
            if i < len(text) and text[i] in self.SANSKRIT_MARKS:
                if i + 1 >= len(text) or text[i+1] in self.TERMINATOR_CHARS:
                    result.append(text[i])
                    i += 1
                    continue
            
            # Check for vowel 'A' (long vowel only if preceded by lowercase)
            if i < len(text) and text[i] == 'A':
                if i > 0 and i - 1 < len(text) and text[i-1].islower():
                    result.append('A')  # Keep for long vowel
                else:
                    result.append('a')  # Normalize all-caps
                i += 1
                continue
            
            # Check for multi-char consonant
            found_multichar = False
            for length in [4, 3, 2]:
                if i + length <= len(text):
                    segment = text[i:i+length]
                    if segment.lower() in self.alphabet.CONSONANTS:
                        result.append(segment.lower())
                        i += length
                        found_multichar = True
                        break
            
            if found_multichar:
                continue
            
            # Single character
            if text[i].isupper():
                # Check if it's a potential Sanskrit capital (N, T, D, S)
                if text[i] in ['N', 'T', 'D', 'S'] and i+1 < len(text):
                    next_char = text[i+1]
                    # If followed by vowel (not 'h' or 'a'), it's Sanskrit
                    if next_char.islower() and next_char not in ['h', 'a']:
                        # Convert "Ni" to "Nai" so parser sees "Na" + "i" vowel
                        result.append(text[i] + 'a')
                        i += 1
                        continue
                
                # Otherwise normalize if it's a consonant
                if text[i].lower() in self.alphabet.CONSONANTS:
                    result.append(text[i].lower())
                else:
                    result.append(text[i])
            else:
                result.append(text[i])
            i += 1
        
        return ''.join(result)

