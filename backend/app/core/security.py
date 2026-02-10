import secrets
import string

def generate_otp(length: int = 6) -> str:
    characters = string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))
