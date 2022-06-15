# Importing the neccassary Libraries
from rich.console import Console
from rich.table import Table
from getpass import getpass
from components.encrypt import Encryptor
import cryptography

# Creating the Input/Output Class


class IO:

    # Constructor
    def __init__(self) -> None:

        # Creating a Console Instance
        self.CONSOLE = Console()

    # Getting the Master Password
    def get_master_password(self) -> str:

        # Returning the Master Password
        pwd = getpass("Enter Master Password ➡️  ")

        # Creating the Encryptor instance with the Master Password
        self.CRYPTOR = Encryptor(pwd)

        # Returning the Master Password
        return pwd

    # Formatting the Passwords in a Table
    def format_and_print_pwd(self, PWD_LIST: list) -> None:

        # Creating the Table
        table = Table()

        # Creating the Password, Email, Username, URL, Service Columns
        table.add_column("Password", style="cyan")
        table.add_column("Email", style="magenta")
        table.add_column("Username", style="green")
        table.add_column("URL", style="cyan")
        table.add_column("App", style="magenta")

        # Trying to Add a Row for Each Password Founded
        try:
            
            # Looping through the Passwords
            for arg in PWD_LIST:

                # Decrypting the Password
                dec_pwd = self.CRYPTOR.decrypt(arg[0])

                # Adding the Row to the Table
                table.add_row(dec_pwd, arg[1], arg[2], arg[3], arg[4])

            # Print the Result
            self.CONSOLE.print(table)
            print()

        # If the Decryption Fails, throw an Error
        except cryptography.fernet.InvalidToken:

            # Printing the Error Message
            self.CONSOLE.print("[red]❌ Invalid Signature![/red]\n")

    # Showing the Menu Options
    def menu(self) -> int:

        # Showing the Menu
        self.CONSOLE.print(
            "[red]###################################[/red]",
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
            "[red]----------------------------------------[/red]",
            sep="\n")

        # Input Loop
        while True:

            # Getting User Input
            DECISION = self.CONSOLE.input("[blue]Enter a Command ➡️[/blue]  ")
            print()

            # Checking if the Input is a Number from 1 to 7
            if DECISION in ["1", "2", "3", "4", "5", "6", "7"]:

                # If, break the Loop
                break

            # Else, printing the Command's Error
            self.CONSOLE.print("[red]❌ Command NOT available![/red]\n")

        # Returning the Command Decision
        return int(DECISION)

    # UI For Creating a New Password
    def create_ui(self) -> dict:

        # Getting User Input
        PWD = getpass("Enter the Password ➡️  ")
        EMAIL = input("Enter the Email ➡️  ")
        USER = input("Enter the Username (if available) ➡️  ")
        URL = input(
            "Enter the Application's URL (if available) ➡️  ")
        APP = input("Enter the Service you are using ➡️  ")
        print()

        # Encrypting the Password
        ENC_PWD = self.CRYPTOR.encrypt(PWD)

        # Returning the Informations in a Dict
        return {
            "pwd": ENC_PWD,
            "email": EMAIL,
            "username": USER,
            "url": URL,
            "app": APP}

    # UI For Updating a Password
    def update_ui(self) -> dict:

        # Getting User Input
        PWD = getpass("Enter the Password ➡️  ")
        EMAIL = input("Enter the Password's Email ➡️  ")
        USER = input("Enter the Password's Username ➡️  ")
        URL = input("Enter the Password's Application URL ➡️  ")
        APP = input("Enter the Password's Service Name ➡️  ")
        NEW_PWD = getpass("\nEnter the New Password ➡️  ")
        print()

        # Encrypting the New Password
        NEW_ENC_PWD = self.CRYPTOR.encrypt(NEW_PWD)

        # Returning the Informations in a Dict
        return {
            "pwd": PWD,
            "email": EMAIL,
            "username": USER,
            "url": URL,
            "app": APP,
            "new_pwd": NEW_ENC_PWD}

    # UI For Deleting a Password
    def delete_ui(self) -> dict:

        # Getting User Input
        PWD = getpass("Enter the Password ➡️  ")
        EMAIL = input("Enter the Email ➡️  ")
        USER = input("Enter the Username ➡️  ")
        URL = input("Enter the Application's URL ➡️  ")
        APP = input("Enter the Service ➡️  ")
        print()

        # Returning the Informations in a Dict
        return {
            "pwd": PWD,
            "email": EMAIL,
            "username": USER,
            "url": URL,
            "app": APP}

    # UI For Searching a Password
    def search_ui(self) -> int:

        # Printing the Menu
        self.CONSOLE.print("[green]Options Available:[/green]",
                           "[blue]1. By URL[/blue]",
                           "[blue]2. By Service[/blue]",
                           "[yellow]3. Exit this Command[/yellow]", sep="\n")

        # Input Loop
        while True:

            # Getting User Input
            OPTION = self.CONSOLE.input("\n[blue]Enter a Command ➡️[/blue]  ")

            # Checking if the Input is a Number from 1 to 3
            if OPTION in ["1", "2", "3"]:

                # If, break the Loop
                break

            # Else, printing the Command's Error
            self.CONSOLE.print("\n❌ [red]Command NOT Valid![/red]")

        # Returning the Command Decision
        return int(OPTION)

    # UI For Listing Passwords
    def list_ui(self) -> int:

        # Printing the Menu
        self.CONSOLE.print("[green]Options Available:[/green]",
                           "[blue]1. By Email[/blue]",
                           "[blue]2. By Username[/blue]",
                           "[yellow]3. Exit this Command[/yellow]", sep="\n")

        # Input Loop
        while True:

            # Getting User Input
            option = self.CONSOLE.input("\n[blue]Enter a Command ➡️[/blue]  ")

            # Checking if the Input is a Number from 1 to 3
            if option in ["1", "2", "3"]:

                # If, break the Loop
                break

            # Else, printing the Command's Error
            self.CONSOLE.print("\n❌ [red]Command NOT Valid![/red]")

        # Returning the Command Decision
        return int(option)
