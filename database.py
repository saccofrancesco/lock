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

        # Returning the Encrypted Value
        return self.public_key.encrypt(
            password.encode(),
            padding.OAEP (
                mgf = padding.MGF1(algorithm = hashes.SHA256()),
                algorithm = hashes.SHA256(),
                label = None
            )
        )

    # Creating the Decryption Method to Decrypt any Encrypted Password with the same Private Key
    def decrypt_password(self, encrypted: bytes) -> str:
        
        # Returning the Decrypted Value
        return self.private_key.decrypt(
            encrypted,
            padding.OAEP (
                mgf = padding.MGF1(algorithm = hashes.SHA256()),
                algorithm = hashes.SHA256(),
                label = None
            )
        ).decode()

    # Creating the varius Progresses Animations' Functions
    def new_pwd_anim(self) -> None:

        self.pwd_fetch(
            "🔏 [blue]Encrypting the Password...[/blue]",
            "✅ [green]Password Succesfully Encrypted and added to the Database[/green]\n",
        )

    def upd_pwd_s_anim(self) -> None:

        self.del_pwd(
            "⬆️ [yellow]Updating the Password...[/yellow]",
            "✅ [green]Pasword Succesfully Updated[/green]\n",
        )

        # Adding Delay
        time.sleep(0.75)

    def del_pwd_s_anim(self) -> None:

        self.del_pwd(
            "❌ [red]Deleting the Password...[/red]",
            "✅ [green]Pasword Succesfully Deleted[/green]\n",
        )

    def del_pwd(self, arg0, arg1):
        self.exit_sequence(
            0.2, "🔭 [blue]Searching the Password...[/blue]"
        )

        self.console.print(
            "✅ [green]Password Succesfully Founded[/green]"
        )

        with self.console.status(arg0):
            time.sleep(1.5)
        self.console.print(arg1)
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

    def pwd_not_found_anim(self) -> None:
        self.pwd_fetch(
            "🔭 [blue]Searching the Password...[/blue]",
            "❌ [red]Password NOT Founded[/red]\n",
        )

    def pwd_srch_anim(self) -> None:
        self.pwd_fetch(
            "🔭 [blue]Searching the Passwords...[/blue]",
            "✅ [green]Passwords Succesfully Founded[/green]\n",
        )

    def pwd_fetch_anim(self) -> None:
        self.pwd_fetch(
            "🔭 [blue]Fetching all the Passwords...[/blue]",
            "✅ [green]Passwords Succesfully Founded[/green]\n",
        )

    def pwd_fetch(self, arg0, arg1):
        self.exit_sequence(0.2, arg0)
        self.console.print(arg1)
        time.sleep(0.75)

    def exit_anim(self) -> None:

        self.exit_sequence(
            0.05, "[yellow]Exiting the Program...[/yellow]"
        )

    def exit_sequence(self, arg0, arg1):
        i = 10
        for _ in track(range(i), description="[green]Processing...[/green]"):
            time.sleep(arg0)
        with self.console.status(arg1):
            time.sleep(3)

    # Get the Master Password for the Login in the Database
    def get_master_password(self) -> bool:

        # Getting User Input
        log_pwd = self.console.input("[blue]Enter the Master Password ➡️[/blue]  ").encode()
        print()

        # Storing the Comparison
        self.state = hashlib.sha512(log_pwd).hexdigest() == self.master_pwd

        # Returning the Result of the Comaprison with the right Master Password
        return self.state

    # Displaying Command Option in a Menu and Getting a User input
    def menu(self, state: bool) -> int:

        # Checking if Loged In
        if state:

            self.option_menu(
                "[red]###################################[/red]",
                "[red]Cryptographied Password Manager[/red]",
                "[red]###################################[/red]",
                "[blue]Available Commands:[/blue]",
            )

            self.option_4_list(
                "[green]1. Create a New Password[/green]",
                "[yellow]2. Update a Password[/yellow]",
                "[red]3. Delete a Password[/red]",
                "[blue]4. Search a Password by URL or Service[/blue]",
            )

            self.option_4_print(
                "[blue]5. List Passwords by Email or Username[/blue]",
                "[green]6. Fetch All the Passwords[/green]",
                "[yellow]7. Exit the Program[/yellow]",
                "[red]----------------------------------------[/red]",
            )

            # Input Loop
            while True:

                # Getting User Input
                dec = self.console.input("[blue]Enter a Command ➡️[/blue]  ")
                print()

                if dec in ["1", "2", "3", "4", "5", "6", "7"]:
                    break

                # Printing Command's Error
                self.console.print("[red]❌ Command NOT available![/red]")
                print()

            # Returning the Command Decision
            return int(dec)

        else:

            self.script_exit_message("[red]Wrong Password!!![/red]")

    # Create the Method for a New Password
    def create_new_password(self) -> None:

        # Getting User Input
        pwd = self.console.input("Enter the Password ➡️  ")
        email = self.console.input("Enter the Email ➡️  ")
        username = self.console.input("Enter the Username (if available) ➡️  ")
        url = self.console.input("Enter the Application's URL (if available) ➡️  ")
        app = self.console.input("Enter the Service you are using ➡️  ")
        print()

        # Encrypting the Password
        enc_pwd = self.encrypt_password(pwd)

        # Perform the SQL Command via Cursor
        self.cursor.execute("INSERT INTO passwords VALUES (?, ?, ?, ?, ?)", (enc_pwd, email, username, url, app))

        # Commiting the Changes
        self.connection.commit()

        # Creation Animation
        self.new_pwd_anim()

    # Create the Method for Updating an existing Password
    def update_password(self) -> None:

        # Getting User Input
        pwd = self.console.input("Enter the Password ➡️  ")
        email = self.console.input("Enter the Password's Email ➡️  ")
        username = self.console.input("Enter the Password's Username ➡️  ")
        url = self.console.input("Enter the Password's Application URL ➡️  ")
        app = self.console.input("Enter the Password's Service Name ➡️  ")
        new_pwd = self.console.input("\nEnter the New Password ➡️  ")
        print()

        # Encrypting the New Password
        new_enc_pwd = self.encrypt_password(new_pwd)

        # Searching in ALL the Password the ONE which corrispond to te Password Inputed
        self.cursor.execute("SELECT * FROM passwords WHERE email=? AND username=? AND url=? AND app=?", (email, username, url, app))
        if password_list := self.cursor.fetchall():

            # Saving the Pre Encrypted Password
            pre_enc_pwd = password_list[0][0]

            # Checking if the Encrypted Password Correspond to the One Given and then Updating
            if self.decrypt_password(pre_enc_pwd) == pwd:

                # Updating the Password via SQL Cursor Command 
                self.cursor.execute("UPDATE passwords SET password=? WHERE password=? AND email=? AND username=? AND url=? AND app=?", 
                                   (new_enc_pwd, pre_enc_pwd, email, username, url, app))

                # Commiting the Changes
                self.connection.commit()

                # Update Animation
                self.upd_pwd_s_anim()

        else:
            # Error Animation
            self.pwd_not_found_anim()

    # Create the Method for Deleting an existing Password
    def delete_password(self) -> None:
        
        # Getting User Input
        pwd = self.console.input("Enter the Password ➡️  ")
        email = self.console.input("Enter the Email ➡️  ")
        username = self.console.input("Enter the Username ➡️  ")
        url = self.console.input("Enter the Application's URL ➡️  ")
        app = self.console.input("Enter the Service ➡️  ")
        print()

        # Searching in ALL the Password the ONE which corrispond to te Password Inputed
        self.cursor.execute("SELECT * FROM passwords WHERE email=? AND username=? AND url=? AND app=?", (email, username, url, app))
        if password_list := self.cursor.fetchall():

            # Saving the Pre Encrypted Password
            pre_enc_pwd = password_list[0][0]

            # Checking if the Encrypted Password Correspond to the One Given and then Updating
            if self.decrypt_password(pre_enc_pwd) == pwd:

                # Perform the SQL Command via Cursor
                self.cursor.execute("DELETE from passwords WHERE password=? AND email=? AND username=? AND url=? AND app=?", 
                                   (pre_enc_pwd, email, username, url, app))

                # Commiting the Changes
                self.connection.commit()

                # Delete Animation
                self.del_pwd_s_anim()

        else:
            # Error Animation
            self.pwd_not_found_anim()

    # Create the Searching Method, to filter Password by URL or Service Name (App)
    def search_passwords(self) -> None:

        self.option_menu(
            "[green]Options Available:[/green]",
            "[blue]1. By URL[/blue]",
            "[blue]2. By Service[/blue]",
            "[yellow]3. Exit this Command[/yellow]",
        )

        print()

        # Input Loop
        while True:

            # Getting User Input
            option = self.console.input("[blue]Enter a Command ➡️[/blue]  ")
            print()

            if option in ["1", "2", "3"]:
                break

            # Printing Command's Error
            self.console.print("❌ [red]Command NOT Valid![/red]")
            print()
            continue

        # Handling By URL Option
        if option == "1":
            
            self.password_message_anim(
                "[blue]Enter the Service's URL ➡️[/blue]  ",
                "SELECT * FROM passwords WHERE url=?",
            )

        elif option == "2":

            self.password_message_anim(
                "[blue]Enter the Service's Name ➡️[/blue]  ",
                "SELECT * FROM passwords WHERE app=?",
            )

        elif option == "3":

            # Exit Message
            self.console.print("[yellow]Exiting the Command[/yellow]")
            print()

    # Creating the Method to display passwords with the same Email or Username
    def passwords_lister(self) -> None:

        self.option_menu(
            "[green]Options Available:[/green]",
            "[blue]1. By Email[/blue]",
            "[blue]2. By Username[/blue]",
            "[yellow]3. Exit this Command[/yellow]",
        )

        self.console.print()

        # Input Loop
        while True:

            # Getting User Input
            option = self.console.input("[blue]Enter a Command ➡️[/blue]  ")
            print()

            if option in ["1", "2", "3"]:
                break

            # Printing Command's Error
            self.console.print("❌ [red]Command NOT Valid![/red]")
            print()
            continue

        # Handling By Email Option
        if option == "1":

            self.password_message_anim(
                "[blue]Enter the Account's Email ➡️[/blue]  ",
                "SELECT * FROM passwords WHERE email=?",
            )

        elif option == "2":

            self.password_message_anim(
                "[blue]Enter the Account's Username ➡️[/blue]  ",
                "SELECT * FROM passwords WHERE username=?",
            )

        elif option == "3":

            # Exit Message
            self.console.print("[yellow]Exiting the Command[/yellow]")
            print()

    def option_menu(self, arg0, arg1, arg2, arg3):
        self.option_4_list(
            arg0, arg1, arg2, arg3
        )

    def option_4_list(self, arg0, arg1, arg2, arg3):
        self.option_4_print(
            arg0, arg1, arg2, arg3
        )

    def option_4_print(self, arg0, arg1, arg2, arg3):
        self.console.print(arg0)
        self.console.print(arg1)
        self.console.print(arg2)
        self.console.print(arg3)

    def password_message_anim(self, arg0, arg1):
        search = self.console.input(arg0)
        print()
        self.cursor.execute(arg1, (search, ))
        if password_list := self.cursor.fetchall():
            self.pwd_srch_anim()
            self.format_and_print_pwd(password_list)
        else:
            self.pwd_not_found_anim()

    # Defining the Fetch All method, to see ALL the Passwords in the Database
    def fetch_all_passwords(self) -> None:
        
        # Querying all the Passwords
        self.cursor.execute("SELECT * FROM passwords")

        if password_list := self.cursor.fetchall():
            # Animate the Searching Process
            self.pwd_fetch_anim()

            # Using the Prettier to format the founded Passwords in a Table
            self.format_and_print_pwd(password_list)

        else:
            # Printing an Error Message
            self.pwd_not_found_anim()

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
            
            self.script_exit_message(
                "[yellow]Exiting the Program...[/yellow]"
            )

    # TODO Rename this here and in `menu` and `input_handler`
    def script_exit_message(self, arg0):
        self.console.print(arg0)
        self.connection.commit()
        self.connection.close()
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