import string
import random

def alphanumeric(length=64):
    allowed_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(allowed_chars) for _ in range(length))
