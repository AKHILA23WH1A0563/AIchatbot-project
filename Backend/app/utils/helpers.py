import os
import hashlib
import hmac
import base64

_ITERATIONS = 200_000

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _ITERATIONS)
    return base64.b64encode(salt + dk).decode("utf-8")

def verify_password(password: str, stored: str) -> bool:
    raw = base64.b64decode(stored.encode("utf-8"))
    salt, dk = raw[:16], raw[16:]
    new_dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _ITERATIONS)
    return hmac.compare_digest(dk, new_dk)
