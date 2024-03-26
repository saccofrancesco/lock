# Importing Libraries
import sqlite3
import os
from database.encryptor import encrypt, decrypt

# Storing constants to use in class
DB_PATH: str = os.path.join('database', '.database.db')

# Initialize Global Class' Variables
CONNECTION: sqlite3.Connection = sqlite3.connect(DB_PATH)
CURSOR: sqlite3.Cursor = CONNECTION.cursor()

# Method to always chek if the table is created, if not, do it
def check_and_create_table() -> None:

    # Create the Database Table, if not already existing
    CURSOR.execute(
        '''CREATE TABLE IF NOT EXISTS passwords (password blob,
                                                    email text,
                                                    username text,
                                                    url text,
                                                    service text)''')

    # Committing the Table
    CONNECTION.commit()

# Method for a New Password
def create_password(
        master: str,
        pwd: str,
        email: str,
        username: str,
        url: str,
        service: str) -> None:

    check_and_create_table()

    # Encrypting the password using tha master password
    encrypted_pwd: bytes = encrypt(pwd, master)

    # Perform the SQL Command via Cursor
    CURSOR.execute(
        'INSERT INTO passwords VALUES (?, ?, ?, ?, ?)',
        (encrypted_pwd,
            email,
            username,
            url,
            service))

    # Commiting the Changes
    CONNECTION.commit()

# Method for updating an existing Password
def update_password(
        master: str,
        new_pwd: str,
        email: str,
        username: str,
        url: str,
        service: str) -> None:

    check_and_create_table()

    # Searching the password to update based on given criteria
    CURSOR.execute(
        'SELECT password FROM passwords WHERE email=? AND username=? AND url=? AND service=?',
        (email,
            username,
            url,
            service))
    
    # Checking if the decryption goes well or not
    if decrypt(CURSOR.fetchone(), master)[0]:

        # Encrypting the password using tha master password
        encrypted_pwd = encrypt(new_pwd, master)

        # Perform the SQL Command via Cursor
        CURSOR.execute(
            'UPDATE passwords SET password=? WHERE email=? AND username=? AND url=? AND service=?',
            (encrypted_pwd,
                email,
                username,
                url,
                service))

        # Commiting the Changes
        CONNECTION.commit()

# Method to delete a Password
def delete_password(master: str, email: str, username: str, url: str, service: str) -> None:

    check_and_create_table()

    # Searching the password to update based on given criteria
    CURSOR.execute(
        'SELECT password FROM passwords WHERE email=? AND username=? AND url=? AND service=?',
        (email,
            username,
            url,
            service))
    
    # Checking if the decryption goes well or not
    if decrypt(CURSOR.fetchone(), master)[0]:

        # Perform the SQL Command via Cursor
        CURSOR.execute(
            'DELETE from passwords WHERE email=? AND username=? AND url=? AND service=?',
            (email,
                username,
                url,
                service))

        # Commiting the Changes
        CONNECTION.commit()

# Method to search Passwords
def search_password(master: str, criteria: str, value: str) -> list:

    check_and_create_table()

    # Perform the SQL Command via Cursor
    CURSOR.execute(
        f'SELECT * FROM  passwords WHERE {criteria}=?',
        (value,)
    )

    # Fetching the results
    fetch: list = [password[0] for password in CURSOR.fetchall()]
    
    # Decrypting all the passwords based on the given password
    decrypted_passwords: list = [decrypt(password, master)[1] for password in fetch]

    return decrypted_passwords

# Method to fetch all Passwords
def list_passwords(master: str) -> list:

    check_and_create_table()

    # Perform the SQL Command via Cursor
    CURSOR.execute(f'SELECT * FROM passwords')

    # Fetching the results
    fetch: list = [password[0] for password in CURSOR.fetchall()]

    # Decrypting all the passwords based on the given password
    decrypted_passwords: list = [decrypt(password, master)[1] for password in fetch]

    return decrypted_passwords
