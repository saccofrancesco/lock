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