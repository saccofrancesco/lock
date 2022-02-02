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