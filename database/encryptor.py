# Importing Libraries
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidSignature
import secrets
from typing import Tuple

# Creating the Backend
BACKEND: default_backend = default_backend()

# Deriving the Key from the Password
def derive_key(password: str, salt: bytes, iterations: int = 100_000) -> bytes:
    """
    Derives a cryptographic key from a given password and salt using PBKDF2 with HMAC-SHA512.
    
    Args:
        password (str): The password from which to derive the key.
        salt (bytes): A salt to use in the key derivation process.
        iterations (int): The number of iterations to use in the key derivation process. Defaults to 100,000.

    Returns:
        bytes: The derived key encoded in URL-safe base64.
    """
    kdf: PBKDF2HMAC = PBKDF2HMAC(
        algorithm=hashes.SHA512(), length=32, salt=salt,
        iterations=iterations, backend=BACKEND)
    return b64e(kdf.derive(password.encode()))

# Method dedicated to Passwords Encryption
def encrypt(message: str, password: str, iterations: int = 100_000) -> bytes:
    """
    Encrypts a message using a password. The password is used to derive a key, and the message is encrypted with this key.
    
    Args:
        message (str): The message to be encrypted.
        password (str): The password used to derive the encryption key.
        iterations (int): The number of iterations to use in the key derivation process. Defaults to 100,000.

    Returns:
        bytes: The encrypted message encoded in URL-safe base64, including the salt and iteration count.
    """
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
    """
    Decrypts an encrypted message using a password. The password is used to derive the key for decryption.
    
    Args:
        token (bytes): The encrypted message encoded in URL-safe base64, including the salt and iteration count.
        password (str): The password used to derive the decryption key.
        error_indicator (str): The message to return in case of a decryption failure. Defaults to "Decryption failed".

    Returns:
        Tuple[bool, str]: A tuple containing a boolean indicating success or failure, and the decrypted message or error indicator.
    """
    try:
        decoded: bytes = b64d(token)
        salt: bytes = decoded[:16]
        iter_bytes: bytes = decoded[16:20]
        encrypted_token: bytes = b64e(decoded[20:])
        iterations: int = int.from_bytes(iter_bytes, 'big')
        key: bytes = derive_key(password, salt, iterations)
        decrypted_password: str = Fernet(key).decrypt(encrypted_token).decode()
        return True, decrypted_password
    except InvalidSignature:
        # Decryption failed, return False and the error indicator
        return False, error_indicator
