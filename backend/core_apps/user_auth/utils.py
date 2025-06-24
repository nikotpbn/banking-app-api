import random
import string

def generate_otp(legnth=6) -> str:
    return "".join(random.choices(string.digits, k=legnth))
