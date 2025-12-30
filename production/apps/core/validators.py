import re
from django.core.exceptions import ValidationError

def validate_phone_number(value):
    """
    Validates that the phone number contains exactly 10 digits.
    Raises ValidationError if the format is incorrect.
    """
    # Remove any surrounding whitespace
    value = str(value).strip()
    
    if not value.isdigit():
        raise ValidationError('Phone number must contain only digits.')
        
    if len(value) > 10:
        raise ValidationError('Phone number cannot exceed 10 digits.')
        
    if len(value) < 10:
        raise ValidationError('Phone number must be at least 10 digits.')
