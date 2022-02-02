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

# Storing th Keys
pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open('private_key.pem', 'wb') as f:
    f.write(pem)

pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open('public_key.pem', 'wb') as f:
    f.write(pem)

# Animation
console = Console()

with console.status(":unlock: [blue]Creating the Keys...[/blue]"):
    time.sleep(3)

# Succes Message
console.print(":white_heavy_check_mark: [green]Keys Succesfully Created and Stored[/green]\n")

# Adding Delay
time.sleep(0.75)

# Getting the Future Master Password
pwd = console.input("[blue]Enter the Future Master Password :right_arrow:[/blue]  ").encode()

# Velocity of the Progress Bar
i = 10

# Progres Bar Animation
for _ in track(range(i), description="[green]Processing...[/green]"):
    time.sleep(0.2)
with console.status(":unlock: [blue]Hashing the Password...[/blue]"):
    time.sleep(3)

