import random
import string

def genrate_otp(legnth=6) -> str:
    return "".join(random.choices(string.digits, k=legnth))
