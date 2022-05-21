# Importing the necessaries Libraries
import sqlite3
import cryptography
from components.input_output import IO
from components.encrypt import Encryptor
from rich.console import Console
# Creating the Class


class Database:

    # Defining the Constructor
    def __init__(self) -> None:

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

        # Creating the IO Object
        self.IO = IO()

        # Getting the Master Password
        self.master_pwd = self.IO.get_master_password()

        # Creating the Cryptor Object
        self.cryptor = Encryptor(self.master_pwd)

        # Saving a Console Instance for Class' Pretty Printing
        self.console = Console()

    # Creating the Function to extract in a List the Passwords by different
    # Criteria
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
            self.IO.format_and_print_pwd(pwd_list)

        else:

            # Printing the Error Message
            self.console.print("\n[red]❌ No Results Founded[/red]\n")

    # Create the Method for a New Password
    def create_new_password(self) -> None:

        # Getting User Input
        info = self.IO.create_ui()

        # Perform the SQL Command via Cursor
        self.cursor.execute(
            "INSERT INTO passwords VALUES (?, ?, ?, ?, ?)",
            (info["pwd"],
             info["email"],
             info["username"],
             info["url"],
             info["app"]))

        # Commiting the Changes
        self.connection.commit()

        # Printing Success Message
        self.console.print("[green]✅ Password Created![/green]\n")

    # Create the Method for Updating an existing Password
    def update_password(self) -> None:

        # Getting User Input
        info = self.IO.update_ui()

        # Searching in ALL the Password the ONE which corrispond to te Password
        # Inputed
        self.cursor.execute(
            "SELECT * FROM passwords WHERE email=? AND username=? AND url=? AND app=?",
            (info["email"],
             info["username"],
             info["url"],
             info["app"]))
        if password_list := self.cursor.fetchall():

            # Saving the Pre Encrypted Password
            pre_enc_pwd = password_list[0][0]

            # Checking if the Encrypted Password Correspond to the One Given
            # and then Updating
            try:

                if self.cryptor.decrypt(pre_enc_pwd) == info["pwd"]:

                    # Updating the Password via SQL Cursor Command
                    self.cursor.execute(
                        "UPDATE passwords SET password=? WHERE password=? AND email=? AND username=? AND url=? AND app=?",
                        (info["new_pwd"],
                         pre_enc_pwd,
                         info["email"],
                         info["username"],
                         info["url"],
                         info["app"]))

                    # Commiting the Changes
                    self.connection.commit()

                    # Printing Success Message
                    self.console.print("[green]✅ Password Updated![/green]\n")

            except cryptography.fernet.InvalidToken:

                # Printing Error Message
                self.console.print(
                    "[red]❌ Invalid Signature! Password NOT Updated![/red]\n")

        else:

            # Printing Error Message
            self.console.print("[red]❌ Password NOT Found![/red]\n")

    # Create the Method for Deleting an existing Password
    def delete_password(self) -> None:

        # Getting User Input
        info = self.IO.delete_ui()

        # Searching in ALL the Password the ONE which corrispond to te Password
        # Inputed
        self.cursor.execute(
            "SELECT * FROM passwords WHERE email=? AND username=? AND url=? AND app=?",
            (info["email"],
             info["username"],
             info["url"],
             info["app"]))
        if password_list := self.cursor.fetchall():

            # Saving the Pre Encrypted Password
            pre_enc_pwd = password_list[0][0]

            # Checking if the Encrypted Password Correspond to the One Given
            # and then Updating
            try:

                if self.cryptor.decrypt(pre_enc_pwd) == info["pwd"]:

                    # Perform the SQL Command via Cursor
                    self.cursor.execute(
                        "DELETE from passwords WHERE password=? AND email=? AND username=? AND url=? AND app=?",
                        (pre_enc_pwd,
                         info["email"],
                         info["username"],
                         info["url"],
                         info["app"]))

                    # Commiting the Changes
                    self.connection.commit()

                    # Printing Success Message
                    self.console.print("[green]✅ Password Deleted![/green]\n")

            except cryptography.fernet.InvalidToken:

                # Printing Error Message
                self.console.print(
                    "[red]❌ Invalid Signature! Password NOT Deleted![/red]\n")

        else:

            # Printing Error Message
            self.console.print("[red]❌ Password NOT Found![/red]\n")

    # Create the Searching Method, to filter Password by URL or Service Name
    def search_passwords(self) -> None:

        # Printing the Menu and Saving the Decision
        option = self.IO.search_ui()

        # Handling By URL Option
        if option == 1:

            # Getting the Input Value
            url = self.console.input("\n[blue]Enter the URL ➡️[/blue]  ")

            # Extracting and Showing the Results
            self.extract_and_show_passwords("url", url)

        elif option == 2:

            # Getting the Input Value
            service = self.console.input(
                "\n[blue]Enter the Service's Name ➡️[/blue]  ")

            # Extracting and Showing the Results
            self.extract_and_show_passwords("app", service)

        elif option == "3":

            # Exit Message
            self.console.print("\n[yellow]Exiting the Command...[/yellow]\n")

    # Creating the Method to display passwords with the same Email or Username
    def passwords_lister(self) -> None:

        # Printing the Menu and Saving the Decision
        option = self.IO.list_ui()

        # Handling By Email Option
        if option == 1:

            # Getting the Input Value
            email = self.console.input(
                "\n[blue]Enter the Account's Email ➡️[/blue]  ")

            # Extracting and Showing the Results
            self.extract_and_show_passwords("email", email)

        elif option == 2:

            # Getting the Input Value
            username = self.console.input(
                "\n[blue]Enter the Account's Username ➡️[/blue]  ")

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
        self.IO.format_and_print_pwd(password_list)

    # Defining a Handler for the Menu's Input
    def input_handler(self) -> None:

        # Showing the Menu
        dec = self.IO.menu()

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

    # Creating the Program's Loop
    while True:

        # Handling the User's Input
        db.input_handler()
