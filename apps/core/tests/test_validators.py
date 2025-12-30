from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from apps.core.validators import validate_phone_number

class PhoneNumberValidatorTests(SimpleTestCase):
    def test_valid_phone_number(self):
        """Test that a valid 10-digit number passes validation."""
        try:
            validate_phone_number('1234567890')
        except ValidationError:
            self.fail("validate_phone_number raised ValidationError unexpectedly!")

    def test_invalid_length_short(self):
        """Test that a number with fewer than 10 digits fails."""
        with self.assertRaisesMessage(ValidationError, 'Phone number must be at least 10 digits.'):
            validate_phone_number('123456789')

    def test_invalid_length_long(self):
        """Test that a number with more than 10 digits fails."""
        with self.assertRaisesMessage(ValidationError, 'Phone number cannot exceed 10 digits.'):
            validate_phone_number('12345678901')

    def test_non_numeric(self):
        """Test that non-numeric characters fail."""
        with self.assertRaisesMessage(ValidationError, 'Phone number must contain only digits.'):
            validate_phone_number('123456789a')
            
    def test_with_special_chars(self):
        """Test that special characters like hyphens fail (strict 10 digits only)."""
        with self.assertRaisesMessage(ValidationError, 'Phone number must contain only digits.'):
            validate_phone_number('123-456-7890')

    def test_empty_string(self):
        """Test that empty string fails."""
        with self.assertRaises(ValidationError):
            validate_phone_number('')
