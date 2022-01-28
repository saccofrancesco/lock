# Cryptographied Password Manager
This is a Cryptographied Password Manager, a tool for storing Passwords in your Local machine. 
It Relays on Sqlite3 Standard Python Library, the Cryptography Module, the hashlib Standard Python Library, and the Rich Python's Library. 
It stores Passwords in a Local Database in a Crypted Way. It uses Asymmetric Encryption to encrypt, with a Public Key, any given Password and store it in the Database. 
Then, if you want to visualize it, you can run the Commands and the Program will decrypt the Password, with a Private Key, and display it in a Decrypted way.

## Set Up
Download the ZIP Folder, or Clone the Repository with:
```
git clone https://github.com/TonicStark/Cryptographied-Password-Manager.git
```

Then install the dependencies in a virtualenv, you can create one via `python -m venv <name of the virtualenv>`, with:
```
pip install -r requirments.txt
```

Now, you need to run the `keys.py` file and then **DELETE** it. This file will populate the `public_key.pem` and `private_key.pem` files with personalized text. Those are your **Public** and **Private Keys**. Now open the `public_key.pem` and `private_key.pem` files and look at them.

The `public_key.pem` can be public so you don't have to keep it secret. The `private_key.pem` mustn't be public. **DON'T MAKE IT PUBLIC** because this is the only way you have to decrypt YOUR passwords. Is the only way to reverse the process.

If you try to access the database in other ways, you can see that the passwords are stored in an encrypted way.

Now open the `master.py` file, run it and then delete it or, if you want, you can keep it to, in future change your password (less secure).
This file will populate the `master.key` file with a hashed version of the password you gave in input to the file. This is the only password you will now have to remember to access all the other ones stored in the database.

## Start the Program
Now you have only to start the program and you will have a nice command-line interface to store, update and delete your passwords. You can also search your passwords and list them by various Options. Follow the Commands' instructions and you won't face any problems. **Happy Encryption!**