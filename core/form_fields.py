from django import forms

from core.utils import normalize_phone_number_if_possible


class PhoneNumberField(forms.CharField):
    default_error_messages = {
        "required": "Телефонскиот број е задолжителен.",
        "invalid": "Телефонскиот број не е валиден.",
    }

    def clean(self, value):
        value = super().clean(value)
        normalized = normalize_phone_number_if_possible(value)
        if not normalized:
            raise forms.ValidationError(self.error_messages["invalid"])
        return normalized
