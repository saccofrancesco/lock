# Importing the necessaries Libraries
import sqlite3
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from rich.console import Console
from rich.progress import track
from rich.table import Table
import time
import hashlib
import os

# Creating the Class
class Database:
    
    # Defining the Constructor
    def __init__(self) -> None:

        # Login State Variable
        self.state = False

        # Initialize Global Class' Variables
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()

        # Create the Database Table, if not already existing
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS passwords (password blob,
                                                                     email text,
                                                                     username text,
                                                                     url text,
                                                                     app text)""")
        
        # Committing the Table
        self.connection.commit()

        # Reading the Keys and save them to a self. Variable
        with open(os.environ.get("PRIVATE_KEY"), "rb") as key_file:
            self.private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        with open("public_key.pem", "rb") as key_file:
            self.public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )

        # Reading the Password and save it to a self. Variable
        self.master_pwd = os.environ.get("PASSWORD_HASH")

        # Saving a Console Instance for Class' Pretty Printing
        self.console = Console()

    # Creating the Encryption Method to Encrypt any given Password with the same Public Key
    def encrypt_password(self, password: bytes) -> bytes:

        # Encrypting the Given Password with the Public Key
        encrypted = self.public_key.encrypt(
            password.encode(),
            padding.OAEP (
                mgf = padding.MGF1(algorithm = hashes.SHA256()),
                algorithm = hashes.SHA256(),
                label = None
            )
        )

        # Returning the Encrypted Value
        return encrypted