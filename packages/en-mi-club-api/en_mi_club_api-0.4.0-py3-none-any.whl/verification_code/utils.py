import random


# Sacada de chatgpt
def generate_six_digit_code() -> str:
    """Generate a six-digit code as a string."""
    return f"{random.randint(0, 999999):06d}"
