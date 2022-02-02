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

    def pwd_fetch_anim(self) -> None:

        # Velocity of the Progress Bar
        i = 10

        # Progres Bar Animation
        for _ in track(range(i), description="[green]Processing...[/green]"):
            time.sleep(0.2)
        with self.console.status(":telescope: [blue]Fetching all the Passwords...[/blue]"):
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

    # Displaying Command Option in a Menu and Getting a User input
    def menu(self, state: bool) -> int:

        # Checking if Loged In
        if state:

            # Printing Out the Menu
            self.console.print("[red]###################################[/red]")
            self.console.print("[red]Cryptographied Password Manager[/red]")
            self.console.print("[red]###################################[/red]")
            self.console.print("[blue]Available Commands:[/blue]")
            self.console.print("[green]1. Create a New Password[/green]")
            self.console.print("[yellow]2. Update a Password[/yellow]")
            self.console.print("[red]3. Delete a Password[/red]")
            self.console.print("[blue]4. Search a Password by URL or Service[/blue]")
            self.console.print("[blue]5. List Passwords by Email or Username[/blue]")
            self.console.print("[green]6. Fetch All the Passwords[/green]")
            self.console.print("[yellow]7. Exit the Program[/yellow]")
            self.console.print("[red]----------------------------------------[/red]")

            # Input Loop
            while True:

                # Getting User Input
                dec = self.console.input("[blue]Enter a Command :right_arrow:[/blue]  ")
                print()

                if dec == "1" or dec == "2" or dec == "3" or dec == "4" or dec == "5" or dec == "6" or dec == "7":

                    break

                else:

                    # Printing Command's Error
                    self.console.print("[red]:x: Command NOT available![/red]")
                    print()
            
            # Returning the Command Decision
            return int(dec)

        else:

            # Exiting Message
            self.console.print("[red]Wrong Password!!![/red]")

            # Committing any possible Changes
            self.connection.commit()

            # Closing the Connection
            self.connection.close()

            # Exiting Completly the Program
            exit()

    # Create the Method for a New Password
    def create_new_password(self) -> None:

        # Getting User Input
        pwd = self.console.input("Enter the Password :right_arrow:  ")
        email = self.console.input("Enter the Email :right_arrow:  ")
        username = self.console.input("Enter the Username (if available) :right_arrow:  ")
        url = self.console.input("Enter the Application's URL (if available) :right_arrow:  ")
        app = self.console.input("Enter the Service you are using :right_arrow:  ")
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
        pwd = self.console.input("Enter the Password :right_arrow:  ")
        email = self.console.input("Enter the Password's Email :right_arrow:  ")
        username = self.console.input("Enter the Password's Username :right_arrow:  ")
        url = self.console.input("Enter the Password's Application URL :right_arrow:  ")
        app = self.console.input("Enter the Password's Service Name :right_arrow:  ")
        new_pwd = self.console.input("\nEnter the New Password :right_arrow:  ")
        print()

        # Encrypting the New Password
        new_enc_pwd = self.encrypt_password(new_pwd)

        # Searching in ALL the Password the ONE which corrispond to te Password Inputed
        self.cursor.execute("SELECT * FROM passwords WHERE email=? AND username=? AND url=? AND app=?", (email, username, url, app))
        password_list = self.cursor.fetchall()

        # Checking if the List is not Empty
        if password_list:

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
        pwd = self.console.input("Enter the Password :right_arrow:  ")
        email = self.console.input("Enter the Email :right_arrow:  ")
        username = self.console.input("Enter the Username :right_arrow:  ")
        url = self.console.input("Enter the Application's URL :right_arrow:  ")
        app = self.console.input("Enter the Service :right_arrow:  ")
        print()

        # Searching in ALL the Password the ONE which corrispond to te Password Inputed
        self.cursor.execute("SELECT * FROM passwords WHERE email=? AND username=? AND url=? AND app=?", (email, username, url, app))
        password_list = self.cursor.fetchall()

        # Checking if the List is not Empty
        if password_list:
            
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

        # Getting User Input
        self.console.print("[green]Options Available:[/green]")
        self.console.print("[blue]1. By URL[/blue]")
        self.console.print("[blue]2. By Service[/blue]")
        self.console.print("[yellow]3. Exit this Command[/yellow]")
        print()

        # Input Loop
        while True:

            # Getting User Input
            option = self.console.input("[blue]Enter a Command :right_arrow:[/blue]  ")
            print()

            # Verifying if the Command entered is Valid
            if option == "1" or option == "2" or option == "3":

                break

            else:

                # Printing Command's Error
                self.console.print(":x: [red]Command NOT Valid![/red]")
                print()
                continue

        # Creating a Variable to store ALL the Passwords founded
        password_list = []

        # Handling By URL Option
        if option == "1":
            
            # Getting User Input
            search = self.console.input("[blue]Enter the Service's URL :right_arrow:[/blue]  ")
            print()

            # Querying the Password
            self.cursor.execute("SELECT * FROM passwords WHERE url=?", (search,))

            # Saving All the Password founded with the Specified URL
            password_list = self.cursor.fetchall()

            # Checking if the List is not Empty
            if password_list:

                # Animate the Searching Process
                self.pwd_srch_anim()

                # Using the Prettier to format the founded Passwords in a Table
                self.format_and_print_pwd(password_list)
            
            else:

                # Printing an Error Message
                self.pwd_not_found_anim()

        # Handling By Service Name (App) Option
        elif option == "2":

            # Getting User Input
            search = self.console.input("[blue]Enter the Service's Name :right_arrow:[/blue]  ")
            print()

            # Querying the Password
            self.cursor.execute("SELECT * FROM passwords WHERE app=?", (search,))

            # Saving All the Password founded with the Specified Service Name (App)
            password_list = self.cursor.fetchall()

            # Checking if the List is not Empty
            if password_list:

                # Animate the Searching Process
                self.pwd_srch_anim()

                # Using the Prettier to format the founded Passwords in a Table
                self.format_and_print_pwd(password_list)

            else:
                
                # Printing an Error Message
               self.pwd_not_found_anim()
        
        # Handling the Exit Case
        elif option == "3":

            # Exit Message
            self.console.print("[yellow]Exiting the Command[/yellow]")
            print()

    # Creating the Method to display passwords with the same Email or Username
    def passwords_lister(self) -> None:

        # Displaying User Option
        self.console.print("[green]Options Available:[/green]")
        self.console.print("[blue]1. By Email[/blue]")
        self.console.print("[blue]2. By Username[/blue]")
        self.console.print("[yellow]3. Exit this Command[/yellow]")
        self.console.print()

        # Input Loop
        while True:

            # Getting User Input
            option = self.console.input("[blue]Enter a Command :right_arrow:[/blue]  ")
            print()

            # Verifying if the Command entered is Valid
            if option == "1" or option == "2" or option == "3":
                
                break

            else:

                # Printing Command's Error
                self.console.print(":x: [red]Command NOT Valid![/red]")
                print()
                continue
        
        # Creating a Variable to store ALL the Passwords founded
        password_list = []

        # Handling By Email Option
        if option == "1":

            # Getting User Input
            search = self.console.input("[blue]Enter the Account's Email :right_arrow:[/blue]  ")
            print()

            # Querying the Password
            self.cursor.execute("SELECT * FROM passwords WHERE email=?", (search,))

            # Saving All the Password with the Specific Parameter
            password_list = self.cursor.fetchall()

            # Checking if the List is not Empty
            if password_list:

                # Animate the Searching Process
                self.pwd_srch_anim()

                # Using the Prettier to format the founded Passwords in a Table
                self.format_and_print_pwd(password_list)
            
            else:

                # Printing an Error Message
                self.pwd_not_found_anim()

        # Handling By Username Option
        elif option == "2":

            # Getting User Input
            search = self.console.input("[blue]Enter the Account's Username :right_arrow:[/blue]  ")
            print()

            # Querying the Password
            self.cursor.execute("SELECT * FROM passwords WHERE username=?", (search,))

            # Saving All the Password with the Specific Parameter
            password_list = self.cursor.fetchall()

            # Checking if the List is not Empty
            if password_list:

                # Animate the Searching Process
                self.pwd_srch_anim()

                # Using the Prettier to format the founded Passwords in a Table
                self.format_and_print_pwd(password_list)
            
            else:

                # Printing an Error Message
                self.pwd_not_found_anim()

        # Handling the Exit Case
        elif option == "3":

            # Exit Message
            self.console.print("[yellow]Exiting the Command[/yellow]")
            print()

    # Defining the Fetch All method, to see ALL the Passwords in the Database
    def fetch_all_passwords(self) -> None:
        
        # Querying all the Passwords
        self.cursor.execute("SELECT * FROM passwords")

        # Saving All the Passwords
        password_list = self.cursor.fetchall()

        # Checking if the List is not Empty
        if password_list:

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
            
            # Exiting Message
            self.console.print("[yellow]Exiting the Program...[/yellow]")

            # Committing ANY possible Changes
            self.connection.commit()

            # Closing the Connection
            self.connection.close()

            # Complitely Exiting the Program
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
