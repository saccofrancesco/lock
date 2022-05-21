# Importing the Libraries
import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Creating the Encryptor Class


class Encryptor:

    # Initializing the Class
    def __init__(self, password: str):

        # Storing the Password
        self.password = password

        # Creating the Backend
        self.BACKEND = default_backend()

    # Deriving the Key from the Password
    def derive_key(self, salt: bytes, iterations: int = 100_000) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(), length=32, salt=salt,
            iterations=iterations, backend=self.BACKEND)
        return b64e(kdf.derive(self.password.encode()))

    # Creating the Encrypt Method
    def encrypt(
            self,
            message: str,
            iterations: int = 100_000) -> bytes:
        salt = secrets.token_bytes(16)
        key = self.derive_key(salt, iterations)
        return b64e(
            b'%b%b%b' % (
                salt,
                iterations.to_bytes(4, 'big'),
                b64d(Fernet(key).encrypt(message.encode())),
            )
        )

    # Creating the Decrypt Method
    def decrypt(self, token: bytes) -> bytes:
        decoded = b64d(token)
        salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
        iterations = int.from_bytes(iter, 'big')
        key = self.derive_key(salt, iterations)
        return Fernet(key).decrypt(token).decode()
