# Importing Libraries
import sqlite3
import os
from database.encryptor import encrypt, decrypt

# Storing constants to use in class
DB_PATH: str = os.path.join("database", ".database.db")

# Initialize Global Class' Variables
CONNECTION: sqlite3.Connection = sqlite3.connect(DB_PATH)
CURSOR: sqlite3.Cursor = CONNECTION.cursor()


# Method to always chek if the table is created, if not, do it
def check_and_create_table() -> None:
    """
    Ensures that the 'passwords' table exists in the database. If the table does not exist,
    it creates the table with columns for password (encrypted blob), email, username, URL, and service.
    """
    # Create the Database Table, if not already existing
    CURSOR.execute(
        """CREATE TABLE IF NOT EXISTS passwords (password blob,
                                                    email text,
                                                    username text,
                                                    url text,
                                                    service text)"""
    )

    # Committing the Table
    CONNECTION.commit()


# Method for a New Password
def create_password(
    master: str, pwd: str, email: str, username: str, url: str, service: str
) -> None:
    """
    Creates a new password entry in the database. The password is encrypted using the master password before storing.

    Args:
        master (str): The master password used for encrypting the password.
        pwd (str): The password to be stored.
        email (str): The email associated with the password.
        username (str): The username associated with the password.
        url (str): The URL associated with the password.
        service (str): The service associated with the password.
    """
    check_and_create_table()

    # Encrypting the password using tha master password
    encrypted_pwd: bytes = encrypt(pwd, master)

    # Perform the SQL Command via Cursor
    CURSOR.execute(
        "INSERT INTO passwords VALUES (?, ?, ?, ?, ?)",
        (encrypted_pwd, email, username, url, service),
    )

    # Commiting the Changes
    CONNECTION.commit()


# Method for updating an existing Password
def update_password(
    master: str, new_pwd: str, email: str, username: str, url: str, service: str
) -> None:
    """
    Updates an existing password in the database. The new password is encrypted using the master password before storing.

    Args:
        master (str): The master password used for encrypting the new password.
        new_pwd (str): The new password to replace the old one.
        email (str): The email associated with the password.
        username (str): The username associated with the password.
        url (str): The URL associated with the password.
        service (str): The service associated with the password.
    """
    check_and_create_table()

    # Searching the password to update based on given criteria
    CURSOR.execute(
        "SELECT password FROM passwords WHERE email=? AND username=? AND url=? AND service=?",
        (email, username, url, service),
    )

    # Checking if the decryption goes well or not
    if decrypt(CURSOR.fetchone()[0], master)[0]:

        # Encrypting the password using tha master password
        encrypted_pwd = encrypt(new_pwd, master)

        # Perform the SQL Command via Cursor
        CURSOR.execute(
            "UPDATE passwords SET password=? WHERE email=? AND username=? AND url=? AND service=?",
            (encrypted_pwd, email, username, url, service),
        )

        # Commiting the Changes
        CONNECTION.commit()


# Method to delete a Password
def delete_password(
    master: str, email: str, username: str, url: str, service: str
) -> None:
    """
    Deletes a password entry from the database based on the provided criteria.

    Args:
        master (str): The master password used for decrypting and verifying the password to be deleted.
        email (str): The email associated with the password.
        username (str): The username associated with the password.
        url (str): The URL associated with the password.
        service (str): The service associated with the password.
    """
    check_and_create_table()

    # Searching the password to update based on given criteria
    CURSOR.execute(
        "SELECT password FROM passwords WHERE email=? AND username=? AND url=? AND service=?",
        (email, username, url, service),
    )

    # Checking if the decryption goes well or not
    if decrypt(CURSOR.fetchone()[0], master)[0]:

        # Perform the SQL Command via Cursor
        CURSOR.execute(
            "DELETE from passwords WHERE email=? AND username=? AND url=? AND service=?",
            (email, username, url, service),
        )

        # Commiting the Changes
        CONNECTION.commit()


# Method to search Passwords
def search_password(master: str, criteria: str, value: str) -> list:
    """
    Searches for passwords in the database based on the provided criteria and value.
    The passwords are decrypted using the master password before returning.

    Args:
        master (str): The master password used for decrypting the found passwords.
        criteria (str): The field to search by (e.g., 'email', 'username', 'url', or 'service').
        value (str): The value to search for in the specified field.

    Returns:
        list: A list of decrypted passwords matching the search criteria.
    """
    check_and_create_table()

    # Perform the SQL Command via Cursor
    CURSOR.execute(f"SELECT * FROM  passwords WHERE {criteria}=?", (value,))

    # Fetching the results
    fetch: list = [password[0] for password in CURSOR.fetchall()]

    # Decrypting all the passwords based on the given password
    decrypted_passwords: list = [decrypt(password, master)[1] for password in fetch]

    return decrypted_passwords


# Method to fetch all Passwords
def list_passwords(master: str) -> list:
    """
    Fetches all passwords from the database. The passwords are decrypted using the master password before returning.

    Args:
        master (str): The master password used for decrypting the passwords.

    Returns:
        list: A list of all decrypted passwords.
    """
    check_and_create_table()

    # Perform the SQL Command via Cursor
    CURSOR.execute(f"SELECT * FROM passwords")

    # Fetching the results
    fetch: list = [password[0] for password in CURSOR.fetchall()]

    # Decrypting all the passwords based on the given password
    decrypted_passwords: list = [decrypt(password, master)[1] for password in fetch]

    return decrypted_passwords
