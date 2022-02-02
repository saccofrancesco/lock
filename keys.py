# Importing Necessaries Libraries
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from rich.console import Console
from rich.progress import track
import time
import hashlib

# Run this File and then Delete It
# Generate the Private Key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Generate the Public Key form the already Created Private Key
public_key = private_key.public_key()