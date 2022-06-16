# Importing Libraries
from components.input_output import IO
from components.encrypt import Encryptor
from rich.console import Console
import sqlite3
import cryptography

# Creating the Database Class


class Database:

    # Constructor
    def __init__(self) -> None:

        # Initialize Global Class' Variables
        self.CONNECTION = sqlite3.connect("database.db")
        self.CURSOR = self.CONNECTION.cursor()

        # Create the Database Table, if not already existing
        self.CURSOR.execute(
            """CREATE TABLE IF NOT EXISTS passwords (password blob,
                                                                    email text,
                                                                    username text,
                                                                    url text,
                                                                    app text)""")

        # Committing the Table
        self.CONNECTION.commit()

        # Creating the Input/Output Instance
        self.IO = IO()

        # Getting the Master Password
        self.MASTER_PWD = self.IO.get_master_password()

        # Creating the Cryptor Object, using the Master Password
        self.CRYPTOR = Encryptor(self.MASTER_PWD)

        # Saving a Console Instance for Class' Pretty Printing
        self.CONSOLE = Console()

    # Creating the Function to extract in a List the Passwords by different
    # Criteria
    def extract_passwords(self, criteria: str, value: str) -> list:

        # Checking the Criteria
        # By Email
        if criteria == "email":

            # Executing the Query
            self.CURSOR.execute("SELECT * FROM passwords WHERE email = ?",
                                (value,))

        # By Username
        elif criteria == "username":

            # Executing the Query
            self.CURSOR.execute("SELECT * FROM passwords WHERE username = ?",
                                (value,))

        # By URL
        elif criteria == "url":

            # Executing the Query
            self.CURSOR.execute("SELECT * FROM passwords WHERE url = ?",
                                (value,))

        # By App
        elif criteria == "app":

            # Executing the Query
            self.CURSOR.execute("SELECT * FROM passwords WHERE app = ?",
                                (value,))

        # Fetching the Results and Returning Them
        return self.CURSOR.fetchall()

    # Creating a Method to Extract and Show Consistently the Passwords
    def extract_and_show_passwords(self, criteria: str, value: str) -> None:

        # Checking if the List is Empty; if not, print the Passwords
        if PWD_LIST := self.extract_passwords(criteria, value):

            # Formatting and Printing the Results
            print("\n")
            self.IO.format_and_print_pwd(PWD_LIST)

        # If the List is Empty, print an Error Message
        else:

            # Printing the Error Message
            self.CONSOLE.print("\n[red]❌ No Results Founded[/red]\n")

    # Create the Method for a New Password
    def create_new_password(self) -> None:

        # Getting User Input
        INFO = self.IO.create_ui()

        # Perform the SQL Command via Cursor
        self.CURSOR.execute(
            "INSERT INTO passwords VALUES (?, ?, ?, ?, ?)",
            (INFO["pwd"],
             INFO["email"],
             INFO["username"],
             INFO["url"],
             INFO["app"]))

        # Commiting the Changes
        self.CONNECTION.commit()

        # Printing Success Message
        self.CONSOLE.print("[green]✅ Password Created![/green]\n")

    # Create the Method for Updating an existing Password
    def update_password(self) -> None:

        # Getting User Input
        INFO = self.IO.update_ui()

        # Searching in ALL the Password the ONE which corrispond to te Password
        # Inputed
        self.CURSOR.execute(
            "SELECT * FROM passwords WHERE email=? AND username=? AND url=? AND app=?",
            (INFO["email"],
             INFO["username"],
             INFO["url"],
             INFO["app"]))

        # Checking if the List is Empty; if not, fetch the Results
        if password_list := self.CURSOR.fetchall():

            # Saving the Pre Encrypted Password
            pre_enc_pwd = password_list[0][0]

            # Checking if the Encrypted Password Correspond to the One Given
            # and then Updating
            try:
                
                # If the Decryption == the Given Password, Update the Password
                if self.CRYPTOR.decrypt(pre_enc_pwd) == INFO["pwd"]:

                    # Updating the Password via SQL Cursor Command
                    self.CURSOR.execute(
                        "UPDATE passwords SET password=? WHERE password=? AND email=? AND username=? AND url=? AND app=?",
                        (INFO["new_pwd"],
                         pre_enc_pwd,
                         INFO["email"],
                         INFO["username"],
                         INFO["url"],
                         INFO["app"]))

                    # Commiting the Changes
                    self.CONNECTION.commit()

                    # Printing Success Message
                    self.CONSOLE.print("[green]✅ Password Updated![/green]\n")

            # If the Decryption != the Given Password, print an Error Message
            except cryptography.fernet.InvalidToken:

                # Printing Error Message
                self.CONSOLE.print(
                    "[red]❌ Invalid Signature! Password NOT Updated![/red]\n")

        # If the List is Empty, print an Error Message
        else:

            # Printing the Error Message
            self.CONSOLE.print("[red]❌ Password NOT Found![/red]\n")

    # Create the Method for Deleting an existing Password
    def delete_password(self) -> None:

        # Getting User Input
        INFO = self.IO.delete_ui()

        # Searching in ALL the Password the ONE which corrispond to te Password
        # Inputed
        self.CURSOR.execute(
            "SELECT * FROM passwords WHERE email=? AND username=? AND url=? AND app=?",
            (INFO["email"],
             INFO["username"],
             INFO["url"],
             INFO["app"]))

        # Checking if the List is Empty; if not, fetch the Results
        if password_list := self.CURSOR.fetchall():

            # Saving the Pre Encrypted Password
            pre_enc_pwd = password_list[0][0]

            # Checking if the Encrypted Password Correspond to the One Given
            # and then Updating
            try:

                # If the Decryption == the Given Password, Delete the Password
                if self.CRYPTOR.decrypt(pre_enc_pwd) == INFO["pwd"]:

                    # Perform the SQL Command via Cursor
                    self.CURSOR.execute(
                        "DELETE from passwords WHERE password=? AND email=? AND username=? AND url=? AND app=?",
                        (pre_enc_pwd,
                         INFO["email"],
                         INFO["username"],
                         INFO["url"],
                         INFO["app"]))

                    # Commiting the Changes
                    self.CONNECTION.commit()

                    # Printing Success Message
                    self.CONSOLE.print("[green]✅ Password Deleted![/green]\n")

            # If the Decryption != the Given Password, print an Error Message
            except cryptography.fernet.InvalidToken:

                # Printing Error Message
                self.CONSOLE.print(
                    "[red]❌ Invalid Signature! Password NOT Deleted![/red]\n")

        # If the List is Empty, print an Error Message
        else:

            # Printing Error Message
            self.CONSOLE.print("[red]❌ Password NOT Found![/red]\n")

    # Create the Searching Method, to filter Password by URL or Service Name
    def search_passwords(self) -> None:

        # Printing the Menu and Saving the Decision
        OPTION = self.IO.search_ui()

        # Handling By URL Option
        if OPTION == 1:

            # Getting the Input Value
            URL = self.CONSOLE.input("\n[blue]Enter the URL ➡️[/blue]  ")

            # Extracting and Showing the Results
            self.extract_and_show_passwords("url", URL)

        # Handling By Service Name Option
        elif OPTION == 2:

            # Getting the Input Value
            SERVICE = self.CONSOLE.input(
                "\n[blue]Enter the Service's Name ➡️[/blue]  ")

            # Extracting and Showing the Results
            self.extract_and_show_passwords("app", SERVICE)

        # Hnadling the Exit Option
        elif OPTION == 3:

            # Exit Message
            self.CONSOLE.print("\n[yellow]Exiting the Command...[/yellow]\n")

    # Creating the Method to display passwords with the same Email or Username
    def passwords_lister(self) -> None:

        # Printing the Menu and Saving the Decision
        OPTION = self.IO.list_ui()

        # Handling By Email Option
        if OPTION == 1:

            # Getting the Input Value
            EMAIL = self.CONSOLE.input(
                "\n[blue]Enter the Account's Email ➡️[/blue]  ")

            # Extracting and Showing the Results
            self.extract_and_show_passwords("email", EMAIL)

        # Handling By Username Option
        elif OPTION == 2:

            # Getting the Input Value
            USERNAME = self.CONSOLE.input(
                "\n[blue]Enter the Account's Username ➡️[/blue]  ")

            # Extracting and Showing the Results
            self.extract_and_show_passwords("username", USERNAME)

        # Hnadling the Exit Option
        elif OPTION == 3:

            # Exit Message
            self.CONSOLE.print("\n[yellow]Exiting the Command...[/yellow]\n")

    # Defining the Fetch All method, to see ALL the Passwords in the Database
    def fetch_all_passwords(self) -> None:

        # Querying all the Passwords
        self.CURSOR.execute("SELECT * FROM passwords")

        # Fetching the Results
        PASSWORD_LIST = self.CURSOR.fetchall()

        # Using the Prettier to format the founded Passwords in a Table
        self.IO.format_and_print_pwd(PASSWORD_LIST)

    # Defining a Handler for the Menu's Input
    def input_handler(self) -> None:

        # Showing the Menu
        dec = self.IO.menu()

        # Handling Menu Valid Cases
        # Handling the Add Password Option
        if dec == 1:

            # Running the New Password Function
            self.create_new_password()

        # Handling the Update Password Option
        elif dec == 2:

            # Running the Update Password Function
            self.update_password()

        # Handling the Delete Password Option
        elif dec == 3:

            # Running the Delete Password Fucntion
            self.delete_password()

        # Handling the Search Password Option
        elif dec == 4:

            # Running the Search Password/s Function
            self.search_passwords()

        # Handling the List Passwords Option
        elif dec == 5:

            # Runnig the Password Lister Function
            self.passwords_lister()

        # Handling the Fetch All Passwords Option
        elif dec == 6:

            # Running the Password Fetch All Function
            self.fetch_all_passwords()

        # Handling the Exit Option
        elif dec == 7:

            # Exiting Message
            self.CONSOLE.print("[yellow]Exiting the Program...[/yellow]\n")

            # Closing the Connection
            self.CONNECTION.close()

            # Exiting the Program
            exit()


# Defining the Running Main Instance
if __name__ == "__main__":

    # Create a New Database Instance
    DB = Database()

    # Creating the Program's Loop
    while True:

        # Handling the User's Input
        DB.input_handler()
