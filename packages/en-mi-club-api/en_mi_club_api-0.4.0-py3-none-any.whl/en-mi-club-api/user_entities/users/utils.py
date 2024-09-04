""" Utils for user entity. """

import base64
import string
import random


# From CHATGPT
def generate_referral_code(user_id: int, name: str) -> str:
    """
    Generate a unique referral code based on the user's ID and name.
    """
    # Encode the user_id in Base32 (produces a string with uppercase letters and digits)
    encoded_id = (
        base64.b32encode(
            user_id.to_bytes((user_id.bit_length() + 7) // 8, "big")
        )
        .decode("utf-8")
        .rstrip("=")
    )

    # Clean the name to contain only alphanumeric characters and take the first 4 characters
    clean_name = "".join(filter(str.isalnum, name)).upper()

    # If the name is shorter than 4 characters, use the available characters
    prefix = clean_name[:4] if len(clean_name) >= 4 else clean_name

    # Generate a short random string as a suffix (to ensure uniqueness if needed)
    suffix = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=2)
    )

    # Combine all parts to form the referral code
    referral_code = f"{prefix}{encoded_id}{suffix}"

    return referral_code
