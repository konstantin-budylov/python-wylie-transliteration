"""
Validation Service - Application Layer
Provides use cases for Wylie input validation.
"""

from typing import Dict, Any
from ..domain.services.wylie_validator import WylieValidator
from ..domain.value_objects.validation_rules import ValidationResult


class ValidationService:
    """
    Application Service for Extended Wylie validation use cases.
    
    Responsibilities:
    - Coordinate validation workflows
    - Provide high-level validation API
    - Format validation results for consumers
    
    Design Principles:
    - Facade Pattern: Simplifies domain complexity for clients
    - Single Responsibility: Application-level orchestration only
    - Dependency Injection: Validator is injected (testable)
    """
    
    def __init__(self, validator: WylieValidator = None):
        """
        Initialize validation service.
        
        Args:
            validator: Optional validator instance (for testing/DI)
        """
        self.validator = validator or WylieValidator()
    
    def validate_wylie(self, wylie_text: str) -> ValidationResult:
        """
        Validate Extended Wylie input.
        
        Args:
            wylie_text: Wylie transliteration text to validate
        
        Returns:
            ValidationResult with detailed error information
        
        Example:
            >>> service = ValidationService()
            >>> result = service.validate_wylie("bla ma")
            >>> print(result.is_valid)  # True
            >>> print(result.get_error_summary())  # "✓ Valid Extended Wylie"
        """
        if not wylie_text:
            return ValidationResult(is_valid=True, errors=tuple(), warnings=tuple())
        
        return self.validator.validate(wylie_text)
    
    def validate_and_get_report(self, wylie_text: str) -> Dict[str, Any]:
        """
        Validate and return structured report.
        
        Args:
            wylie_text: Wylie text to validate
        
        Returns:
            Dictionary with validation details:
            {
                'is_valid': bool,
                'error_count': int,
                'warning_count': int,
                'errors': [{'type': str, 'message': str, 'position': int, ...}],
                'warnings': [...],
                'summary': str
            }
        
        Example:
            >>> service = ValidationService()
            >>> report = service.validate_and_get_report("xyz123")
            >>> print(report['is_valid'])  # False
            >>> print(report['summary'])   # Human-readable summary
        """
        result = self.validate_wylie(wylie_text)
        
        return {
            'is_valid': result.is_valid,
            'error_count': len(result.errors),
            'warning_count': len(result.warnings),
            'errors': [
                {
                    'type': error.error_type,
                    'position': error.position,
                    'syllable': error.syllable,
                    'message': error.message,
                    'suggestion': error.suggestion
                }
                for error in result.errors
            ],
            'warnings': [
                {
                    'type': warning.error_type,
                    'position': warning.position,
                    'syllable': warning.syllable,
                    'message': warning.message,
                    'suggestion': warning.suggestion
                }
                for warning in result.warnings
            ],
            'summary': result.get_error_summary()
        }
    
    def is_valid_wylie(self, wylie_text: str) -> bool:
        """
        Simple boolean validation check (KISS principle).
        
        Args:
            wylie_text: Wylie text to validate
        
        Returns:
            True if valid, False otherwise
        
        Example:
            >>> service = ValidationService()
            >>> service.is_valid_wylie("bla ma")  # True
            >>> service.is_valid_wylie("xyz123")  # False
        """
        return self.validate_wylie(wylie_text).is_valid
    
    def get_validation_errors(self, wylie_text: str) -> list:
        """
        Get list of validation error messages.
        
        Args:
            wylie_text: Wylie text to validate
        
        Returns:
            List of error message strings
        
        Example:
            >>> service = ValidationService()
            >>> errors = service.get_validation_errors("xyz123")
            >>> for error in errors:
            ...     print(error)
        """
        result = self.validate_wylie(wylie_text)
        return [str(error) for error in result.errors]
    
    def validate_batch(self, wylie_texts: list) -> list:
        """
        Validate multiple Wylie texts (DRY principle).
        
        Args:
            wylie_texts: List of Wylie texts to validate
        
        Returns:
            List of ValidationResult objects
        
        Example:
            >>> service = ValidationService()
            >>> texts = ["bla ma", "sangs rgyas", "xyz123"]
            >>> results = service.validate_batch(texts)
            >>> for text, result in zip(texts, results):
            ...     print(f"{text}: {result.is_valid}")
        """
        return [self.validate_wylie(text) for text in wylie_texts]

