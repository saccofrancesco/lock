# Importing the necessaries Libraries
import sqlite3
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from rich.console import Console
from rich.table import Table
import hashlib
from getpass import getpass
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
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS passwords (password blob,
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

    # Creating the Encryption Method to Encrypt any given Password with the
    # same Public Key
    def encrypt_password(self, password: bytes) -> bytes:

        # Returning the Encrypted Value
        return self.public_key.encrypt(
            password.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    # Creating the Decryption Method to Decrypt any Encrypted Password with
    # the same Private Key
    def decrypt_password(self, encrypted: bytes) -> str:

        # Returning the Decrypted Value
        return self.private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()

    # Creating the Formatting function to Output all the listed Passwords in a
    # Table
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

    # Creating the Function to extract in  a List the Passwords by different Criteria
    def extract_passwords(self, criteria: str, value: str) -> list:
            
            # Creating the List to Store the Results
            pwd_list = []
    
            # Checking the Criteria
            if criteria == "email":
    
                # Executing the Query
                self.cursor.execute("SELECT * FROM passwords WHERE email = ?",
                                    (value,))
    
            elif criteria == "username":
    
                # Executing the Query
                self.cursor.execute("SELECT * FROM passwords WHERE username = ?",
                                    (value,))
    
            elif criteria == "url":
    
                # Executing the Query
                self.cursor.execute("SELECT * FROM passwords WHERE url = ?",
                                    (value,))
    
            elif criteria == "app":
    
                # Executing the Query
                self.cursor.execute("SELECT * FROM passwords WHERE app = ?",
                                    (value,))
    
            # Fetching the Results
            pwd_list = self.cursor.fetchall()
    
            # Returning the Results
            return pwd_list

    # Creating a Method to Extract and Show Consistently the Passwords
    def extract_and_show_passwords(self, criteria: str, value: str) -> None:
            
            # Extracting the Passwords
            pwd_list = self.extract_passwords(criteria, value)
    
            # Checking if there are any Results
            if len(pwd_list) > 0:
    
                # Formatting and Printing the Results
                print("\n")
                self.format_and_print_pwd(pwd_list)
    
            else:
    
                # Printing the Error Message
                self.console.print("\n[red]❌ No Results Founded[/red]\n")

    # Get the Master Password for the Login in the Database
    def get_master_password(self) -> bool:

        # Getting User Input
        log_pwd = getpass("Enter the Master Password ➡️  ").encode()
        print()

        # Storing the Comparison
        self.state = hashlib.sha512(log_pwd).hexdigest() == self.master_pwd

        # Returning the Result of the Comaprison with the right Master Password
        return self.state

    # Displaying Command Option in a Menu and Getting a User input
    def menu(self, state: bool) -> int:

        # Checking if Loged In
        if state:

            # Showing the Menu
            self.console.print("[red]###################################[/red]",
                "[red]Cryptographied Password Manager[/red]",
                "[red]###################################[/red]",
                "[blue]Available Commands:[/blue]",
                "[green]1. Create a New Password[/green]",
                "[yellow]2. Update a Password[/yellow]",
                "[red]3. Delete a Password[/red]",
                "[blue]4. Search a Password by URL or Service[/blue]",
                "[blue]5. List Passwords by Email or Username[/blue]",
                "[green]6. Fetch All the Passwords[/green]",
                "[yellow]7. Exit the Program[/yellow]",
                "[red]----------------------------------------[/red]", sep = "\n")

            # Input Loop
            while True:

                # Getting User Input
                dec = self.console.input("[blue]Enter a Command ➡️[/blue]  ")
                print()

                if dec in ["1", "2", "3", "4", "5", "6", "7"]:
                    break

                # Printing Command's Error
                self.console.print("[red]❌ Command NOT available![/red]\n")

            # Returning the Command Decision
            return int(dec)

        else:

            # Printing Error Message
            self.console.print("[red]❌ You are NOT Logged In![/red]\n")

    # Create the Method for a New Password
    def create_new_password(self) -> None:

        # Getting User Input
        pwd = getpass("Enter the Password ➡️  ")
        email = self.console.input("Enter the Email ➡️  ")
        username = self.console.input("Enter the Username (if available) ➡️  ")
        url = self.console.input(
            "Enter the Application's URL (if available) ➡️  ")
        app = self.console.input("Enter the Service you are using ➡️  ")
        print()

        # Encrypting the Password
        enc_pwd = self.encrypt_password(pwd)

        # Perform the SQL Command via Cursor
        self.cursor.execute(
            "INSERT INTO passwords VALUES (?, ?, ?, ?, ?)",
            (enc_pwd,
             email,
             username,
             url,
             app))

        # Commiting the Changes
        self.connection.commit()

        # Printing Success Message
        self.console.print("[green]✅ Password Created![/green]\n")

    # Create the Method for Updating an existing Password
    def update_password(self) -> None:

        # Getting User Input
        pwd = getpass("Enter the Password ➡️  ")
        email = self.console.input("Enter the Password's Email ➡️  ")
        username = self.console.input("Enter the Password's Username ➡️  ")
        url = self.console.input("Enter the Password's Application URL ➡️  ")
        app = self.console.input("Enter the Password's Service Name ➡️  ")
        new_pwd = getpass("\nEnter the New Password ➡️  ")
        print()

        # Encrypting the New Password
        new_enc_pwd = self.encrypt_password(new_pwd)

        # Searching in ALL the Password the ONE which corrispond to te Password
        # Inputed
        self.cursor.execute(
            "SELECT * FROM passwords WHERE email=? AND username=? AND url=? AND app=?",
            (email,
             username,
             url,
             app))
        if password_list := self.cursor.fetchall():

            # Saving the Pre Encrypted Password
            pre_enc_pwd = password_list[0][0]

            # Checking if the Encrypted Password Correspond to the One Given
            # and then Updating
            if self.decrypt_password(pre_enc_pwd) == pwd:

                # Updating the Password via SQL Cursor Command
                self.cursor.execute(
                    "UPDATE passwords SET password=? WHERE password=? AND email=? AND username=? AND url=? AND app=?",
                    (new_enc_pwd,
                     pre_enc_pwd,
                     email,
                     username,
                     url,
                     app))

                # Commiting the Changes
                self.connection.commit()

                # Printing Success Message
                self.console.print("[green]✅ Password Updated![/green]\n")

        else:
            
            # Printing Error Message
            self.console.print("[red]❌ Password NOT Found![/red]\n")

    # Create the Method for Deleting an existing Password
    def delete_password(self) -> None:

        # Getting User Input
        pwd = getpass("Enter the Password ➡️  ")
        email = self.console.input("Enter the Email ➡️  ")
        username = self.console.input("Enter the Username ➡️  ")
        url = self.console.input("Enter the Application's URL ➡️  ")
        app = self.console.input("Enter the Service ➡️  ")
        print()

        # Searching in ALL the Password the ONE which corrispond to te Password
        # Inputed
        self.cursor.execute(
            "SELECT * FROM passwords WHERE email=? AND username=? AND url=? AND app=?",
            (email,
             username,
             url,
             app))
        if password_list := self.cursor.fetchall():

            # Saving the Pre Encrypted Password
            pre_enc_pwd = password_list[0][0]

            # Checking if the Encrypted Password Correspond to the One Given
            # and then Updating
            if self.decrypt_password(pre_enc_pwd) == pwd:

                # Perform the SQL Command via Cursor
                self.cursor.execute(
                    "DELETE from passwords WHERE password=? AND email=? AND username=? AND url=? AND app=?",
                    (pre_enc_pwd,
                     email,
                     username,
                     url,
                     app))

                # Commiting the Changes
                self.connection.commit()

                # Printing Success Message
                self.console.print("[green]✅ Password Deleted![/green]\n")

        else:
            
            # Printing Error Message
            self.console.print("[red]❌ Password NOT Found![/red]\n")

    # Create the Searching Method, to filter Password by URL or Service Name
    def search_passwords(self) -> None:

        # Printing the Menu
        self.console.print("[green]Options Available:[/green]",
            "[blue]1. By URL[/blue]",
            "[blue]2. By Service[/blue]",
            "[yellow]3. Exit this Command[/yellow]", sep = "\n")

        # Input Loop
        while True:

            # Getting User Input
            option = self.console.input("\n[blue]Enter a Command ➡️[/blue]  ")

            if option in ["1", "2", "3"]:
                break

            # Printing Command's Error
            self.console.print("\n❌ [red]Command NOT Valid![/red]")

        # Handling By URL Option
        if option == "1":

            # Getting the Input Value
            url = self.console.input("\n[blue]Enter the URL ➡️[/blue]  ")

            # Extracting and Showing the Results
            self.extract_and_show_passwords("url", url)

        elif option == "2":

            # Getting the Input Value
            service = self.console.input("\n[blue]Enter the Service's Name ➡️[/blue]  ")

            # Extracting and Showing the Results
            self.extract_and_show_passwords("app", service)

        elif option == "3":

            # Exit Message
            self.console.print("\n[yellow]Exiting the Command...[/yellow]\n")

    # Creating the Method to display passwords with the same Email or Username
    def passwords_lister(self) -> None: 

        # Printing the Menu
        self.console.print("[green]Options Available:[/green]",
            "[blue]1. By Email[/blue]",
            "[blue]2. By Username[/blue]",
            "[yellow]3. Exit this Command[/yellow]", sep = "\n")

        # Input Loop
        while True:

            # Getting User Input
            option = self.console.input("\n[blue]Enter a Command ➡️[/blue]  ")

            if option in ["1", "2", "3"]:
                break

            # Printing Command's Error
            self.console.print("\n❌ [red]Command NOT Valid![/red]")

        # Handling By Email Option
        if option == "1":

            # Getting the Input Value
            email = self.console.input("\n[blue]Enter the Account's Email ➡️[/blue]  ")

            # Extracting and Showing the Results
            self.extract_and_show_passwords("email", email)

        elif option == "2":

            # Getting the Input Value
            username = self.console.input("\n[blue]Enter the Account's Username ➡️[/blue]  ")

            # Extracting and Showing the Results
            self.extract_and_show_passwords("username", username)

        elif option == "3":

            # Exit Message
            self.console.print("\n[yellow]Exiting the Command...[/yellow]\n")

    # Defining the Fetch All method, to see ALL the Passwords in the Database
    def fetch_all_passwords(self) -> None:

        # Querying all the Passwords
        self.cursor.execute("SELECT * FROM passwords")

        # Fetching the Results
        password_list = self.cursor.fetchall()

        # Using the Prettier to format the founded Passwords in a Table
        self.format_and_print_pwd(password_list)

    # Defining a Handler for the Menu's Input
    def input_handler(self, dec: int) -> None:

        # Handling Menu Valid Cases
        if dec == 1:

            # Running the New Password Function
            self.create_new_password()

        elif dec == 2:

            # Running the Update Password Function
            self.update_password()

        elif dec == 3:

            # Running the Delete Password Fucntion
            self.delete_password()

        elif dec == 4:

            # Running the Search Password/s Function
            self.search_passwords()

        elif dec == 5:

            # Runnig the Password Lister Function
            self.passwords_lister()

        elif dec == 6:

            # Running the Password Fetch All Function
            self.fetch_all_passwords()

        elif dec == 7:

            # Exiting Message
            self.console.print("[yellow]Exiting the Program...[/yellow]\n")

            # Closing the Connection
            self.connection.close()

            # Exiting the Program
            exit()


# Defining the Running Main Instance
if __name__ == "__main__":

    # Create a New Database Instance
    db = Database()

    # Perform the Login
    state = db.get_master_password()

    # Creating the Program's Loop
    while True:

        # Printing, if Loged In, the Menu and returning the User's Input
        dec = db.menu(state)

        # Handling the User's Input
        db.input_handler(dec)
