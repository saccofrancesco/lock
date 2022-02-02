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

    # Creating the Decryption Method to Decrypt any Encrypted Password with the same Private Key
    def decrypt_password(self, encrypted: bytes) -> str:
        
        # Decrypting the Given Encrypted Password with the Private Key
        original_message = self.private_key.decrypt(
            encrypted,
            padding.OAEP (
                mgf = padding.MGF1(algorithm = hashes.SHA256()),
                algorithm = hashes.SHA256(),
                label = None
            )
        )

        # Returning the Decrypted Value
        return original_message.decode()

    # Creating the varius Progresses Animations' Functions
    def new_pwd_anim(self) -> None:

        # Velocity of the Progress Bar
        i = 10

        # Progres Bar Animation
        for _ in track(range(i), description="[green]Processing...[/green]"):
            time.sleep(0.2)
        with self.console.status(":unlock: [blue]Encrypting the Password...[/blue]"):
            time.sleep(3)
        
        # Succes Message
        self.console.print(":white_heavy_check_mark: [green]Password Succesfully Encrypted and added to the Database[/green]\n")
        
        # Adding Delay
        time.sleep(0.75)

    def upd_pwd_s_anim(self) -> None:

        # Velocity of the Progress Bar
        i = 10

        # Progres Bar Animation
        for _ in track(range(i), description="[green]Processing...[/green]"):
            time.sleep(0.2)
        with self.console.status(":telescope: [blue]Searching the Password...[/blue]"):
            time.sleep(3)
        self.console.print(":white_heavy_check_mark: [green]Password Succesfully Founded[/green]")
        with self.console.status(":up_arrow: [yellow]Updating the Password...[/yellow]"):
            time.sleep(1.5)

        # Succes Message
        self.console.print(":white_heavy_check_mark: [green]Pasword Succesfully Updated[/green]\n")

        # Adding Delay
        time.sleep(0.75)

        # Adding Delay
        time.sleep(0.75)

    def del_pwd_s_anim(self) -> None:

        # Velocity of the Progress Bar
        i = 10

        # Progres Bar Animation
        for _ in track(range(i), description="[green]Processing...[/green]"):
            time.sleep(0.2)
        with self.console.status(":telescope: [blue]Searching the Password...[/blue]"):
            time.sleep(3)
        self.console.print(":white_heavy_check_mark: [green]Password Succesfully Founded[/green]")
        with self.console.status(":x: [red]Deleting the Password...[/red]"):
            time.sleep(1.5)

        # Succes Message
        self.console.print(":white_heavy_check_mark: [green]Pasword Succesfully Deleted[/green]\n")

        # Adding Delay
        time.sleep(0.75)

    def pwd_not_found_anim(self) -> None:

        # Velocity of the Progress Bar
        i = 10

        # Progres Bar Animation
        for _ in track(range(i), description="[green]Processing...[/green]"):
            time.sleep(0.2)
        with self.console.status(":telescope: [blue]Searching the Password...[/blue]"):
            time.sleep(3)

        # Error Message
        self.console.print(":x: [red]Password NOT Founded[/red]\n")

        # Adding Delay
        time.sleep(0.75)

    # Creating the Formatting function to Output all the listed Passwords in a Table
    def format_and_print_pwd(self, pwd_list: list) -> None:

        # Creating the Table
        table = Table()

        # Creating the Columns
        table.add_column("Password", style="cyan")
        table.add_column("Email", style="magenta")
        table.add_column("Username", style="green")
        table.add_column("URL", style="cyan")
        table.add_column("App", style="magenta")

        # Add a Row for Each Password Founded
        for row in pwd_list:
            dec_pwd = self.decrypt_password(row[0])
            table.add_row(dec_pwd, row[1], row[2], row[3], row[4])

        # Printing the Result
        self.console.print(table)
        print()

    def pwd_srch_anim(self) -> None:

        # Velocity of the Progress Bar
        i = 10

        # Progres Bar Animation
        for _ in track(range(i), description="[green]Processing...[/green]"):
            time.sleep(0.2)
        with self.console.status(":telescope: [blue]Searching the Passwords...[/blue]"):
            time.sleep(3)

        # Succes Message
        self.console.print(":white_heavy_check_mark: [green]Passwords Succesfully Founded[/green]\n")

        # Adding Delay
        time.sleep(0.75)

    def exit_anim(self) -> None:

        # Velocity of the Progress Bar
        i = 10

        # Progres Bar Animation
        for _ in track(range(i), description="[green]Processing...[/green]"):
            time.sleep(0.05)
        with self.console.status("[yellow]Exiting the Program...[/yellow]"):
            time.sleep(3)

    # Get the Master Password for the Login in the Database
    def get_master_password(self) -> bool:

        # Getting User Input
        log_pwd = self.console.input("[blue]Enter the Master Password :right_arrow:[/blue]  ").encode()
        print()

        # Storing the Comparison
        self.state = hashlib.sha512(log_pwd).hexdigest() == self.master_pwd

        # Returning the Result of the Comaprison with the right Master Password
        return self.state

    