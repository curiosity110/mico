import logging

import phonenumbers

logger = logging.getLogger(__name__)


def normalize_phone_number_if_possible(phone_number: str) -> str:
    """
    Normalize a phone number to E.164 format for Macedonia.
    If the phone number is invalid or cannot be normalized, it returns the original phone number.
    """
    logger.info(f"Normalizing phone number: {phone_number}")

    try:
        parsed_number = phonenumbers.parse(phone_number, "MK")

        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

    except phonenumbers.NumberParseException:
        pass

    logger.warning(f"Failed to parse phone number: {phone_number}")

    return phone_number
