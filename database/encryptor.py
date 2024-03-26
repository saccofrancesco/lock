# Importing Libraries
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets
from typing import Tuple

# Creating the Backend
BACKEND: default_backend = default_backend()

# Deriving the Key from the Password
def derive_key(password: str, salt: bytes, iterations: int = 100_000) -> bytes:
    kdf: PBKDF2HMAC = PBKDF2HMAC(
        algorithm=hashes.SHA512(), length=32, salt=salt,
        iterations=iterations, backend=BACKEND)
    return b64e(kdf.derive(password.encode()))

# Method dedicated to Passwords Encryption
def encrypt(message: str, password: str, iterations: int = 100_000) -> bytes:
        salt: bytes = secrets.token_bytes(16)
        key: bytes = derive_key(password, salt, iterations)
        encrypted_message: bytes = Fernet(key).encrypt(message.encode())
        return b64e(
            b'%b%b%b' % (
                salt,
                iterations.to_bytes(4, 'big'),
                b64d(encrypted_message),
            )
        )

# Method dedicated to Passwords Decryption
def decrypt(token: bytes, password: str, error_indicator: str = "Decryption failed") -> Tuple[bool, str]:
    try:
        decoded: bytes = b64d(token)
        salt: bytes = decoded[:16]
        iter_bytes: bytes = decoded[16:20]
        encrypted_token: bytes = b64e(decoded[20:])
        iterations: int = int.from_bytes(iter_bytes, 'big')
        key: bytes = derive_key(password, salt, iterations)
        decrypted_password: str = Fernet(key).decrypt(encrypted_token).decode()
        return True, decrypted_password
    except Exception:
        # Decryption failed, return False and the error indicator
        return False, error_indicator
