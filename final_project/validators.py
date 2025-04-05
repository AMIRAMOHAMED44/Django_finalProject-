# final_project/validators.py
from django.core.exceptions import ValidationError
import re

class EgyptianPhoneNumberValidator:
    def __call__(self, value):
        """
        Validates Egyptian phone numbers
        Formats: +201234567890 or 01234567890 or 1023456789 (11 digit)
        """
        pattern = r'^(\+20|0)?1[0-25-9]\d{8}$'
        if not re.match(pattern, value):
            raise ValidationError('يجب أن يكون رقم هاتف مصري صالح (مثال: +201234567890 أو 01234567890)')