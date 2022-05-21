# Importing the neccassary Libraries
from rich.console import Console
from rich.table import Table
from getpass import getpass
import cryptography
from components.encrypt import Encryptor

# Creating the Input/Output Class
class IO:

    # Initializing the IO Class
    def __init__(self):

        # Creating the Console Object
        self.console = Console()

    # Getting the Master Password
    def get_master_password(self) -> str:

        # Returning the Master Password
        pwd = getpass("Enter Master Password ➡️ ")

        # Creating the Encryptor Object
        self.cryptor = Encryptor(pwd)

        # Returning the Master Password
        return pwd

    # Formatting the Passwords in a Table
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
        try:

            for row in pwd_list:
                dec_pwd = self.cryptor.decrypt(row[0])
                table.add_row(dec_pwd, row[1], row[2], row[3], row[4])

            # Printing the Result
            self.console.print(table)
            print()

        except cryptography.fernet.InvalidToken:

            # Printing the Error Message
            self.console.print("[red]❌ Invalid Signature![/red]\n")

    # Showing the Menu Options
    def menu(self) -> int:

        # Showing the Menu
        self.console.print(
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
            dec = self.console.input("[blue]Enter a Command ➡️[/blue]  ")
            print()

            if dec in ["1", "2", "3", "4", "5", "6", "7"]:
                break

            # Printing Command's Error
            self.console.print("[red]❌ Command NOT available![/red]\n")

        # Returning the Command Decision
        return int(dec)

    # UI For Creating a New Password
    def create_ui(self) -> dict:

        # Getting User Input
        pwd = getpass("Enter the Password ➡️  ")
        email = self.console.input("Enter the Email ➡️  ")
        username = self.console.input("Enter the Username (if available) ➡️  ")
        url = self.console.input(
            "Enter the Application's URL (if available) ➡️  ")
        app = self.console.input("Enter the Service you are using ➡️  ")
        print()

        # Encrypting the Password
        enc_pwd = self.cryptor.encrypt(pwd)

        # Returning the Informations in a Dict
        return {"pwd": enc_pwd, "email": email, "username": username, "url": url, "app": app}
    
    # UI For Updating a Password
    def update_ui(self) -> dict:

        # Getting User Input
        pwd = getpass("Enter the Password ➡️  ")
        email = self.console.input("Enter the Password's Email ➡️  ")
        username = self.console.input("Enter the Password's Username ➡️  ")
        url = self.console.input("Enter the Password's Application URL ➡️  ")
        app = self.console.input("Enter the Password's Service Name ➡️  ")
        new_pwd = getpass("\nEnter the New Password ➡️  ")
        print()

        # Encrypting the New Password
        new_enc_pwd = self.cryptor.encrypt(new_pwd)

        # Returning the Informations in a Dict
        return {"pwd": pwd, "email": email, "username": username, "url": url, "app": app, "new_pwd": new_enc_pwd}

    # UI For Deleting a Password
    def delete_ui(self) -> dict:

        # Getting User Input
        pwd = getpass("Enter the Password ➡️  ")
        email = self.console.input("Enter the Email ➡️  ")
        username = self.console.input("Enter the Username ➡️  ")
        url = self.console.input("Enter the Application's URL ➡️  ")
        app = self.console.input("Enter the Service ➡️  ")
        print()

        # Returning the Informations in a Dict
        return {"pwd": pwd, "email": email, "username": username, "url": url, "app": app}

    # UI For Searching a Password
    def search_ui(self) -> int:

        # Printing the Menu
        self.console.print("[green]Options Available:[/green]",
                           "[blue]1. By URL[/blue]",
                           "[blue]2. By Service[/blue]",
                           "[yellow]3. Exit this Command[/yellow]", sep="\n")

        # Input Loop
        while True:

            # Getting User Input
            option = self.console.input("\n[blue]Enter a Command ➡️[/blue]  ")

            if option in ["1", "2", "3"]:
                break

            # Printing Command's Error
            self.console.print("\n❌ [red]Command NOT Valid![/red]")

        # Returning the Command Decision
        return int(option)

    # UI For Listing Passwords
    def list_ui(self) -> int:

        # Printing the Menu
        self.console.print("[green]Options Available:[/green]",
                           "[blue]1. By Email[/blue]",
                           "[blue]2. By Username[/blue]",
                           "[yellow]3. Exit this Command[/yellow]", sep="\n")

        # Input Loop
        while True:

            # Getting User Input
            option = self.console.input("\n[blue]Enter a Command ➡️[/blue]  ")

            if option in ["1", "2", "3"]:
                break

            # Printing Command's Error
            self.console.print("\n❌ [red]Command NOT Valid![/red]")

        # Returning the Command Decision
        return int(option)