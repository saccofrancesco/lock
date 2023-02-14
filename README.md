# Cryptographied Password Manager
Cryptographied Password Manager is a tool for storing Encrypted Passwords in your Local machine. 

## Set Up

### Build by Yourself
Download the ZIP Folder, or Clone the Repository with:
```
git clone https://github.com/TonicStark/cryptographied-password-manager.git
```

Then install the dependencies in a virtualenv, you can create one via `python -m venv <name of the virtualenv>`, with:
```
pip install -r requirements.txt
```
In the *virtualenv*, run the following command:
```
pyinstaller --onefile .\main.py
```
this will **build** the `main.py` file, as a **single** *executable*.
When you finish the build process, you should a *repo* like this:
```
.
└── cryptographied-password-manager/
    ├── build
    ├── components
    ├── dist/
    │   └── passwords.exe
    ├── README Translation
    ├── venv
    ├── .gitignore
    ├── main.py
    ├── README.md
    └── requirements.txt
```
Inside the `dist/` you should have a **file**, `passwords.exe` which you can **execute** as a single program, without having to *activate* the *virtualenv* each time.

To use it in **every** path of your system, you have to add the `.\cryptographied-password-manager\dist\` folder to your *Computer Path*: [here](https://chlee.co/how-to-setup-environment-variables-for-windows-mac-and-linux/) there's a **guide** on how to do it.

## Download (Windows only)
Else, you can *download* in the **Release** section, the *builded* file, ready to be added to your *System Path* to **use it!**

## Personalization
When starting the script for the **FIRST TIME**, choose a **Password** to use as the **_Master Password_** and **remember it**. **EACH time** you want to **Log In** use it and **NEVER** change it. The Master Password is used to **encrypt** the Passwords and also to **decrypt** them. **_Don't write it in the file or share it with anyone._** Only remember it, enter it and the program will derive a key to encrypt and decrypt your Passwords.

# Start the Program
Now you have only to start the program and you will have a nice command-line interface to store, update and delete your passwords. You can also search for your passwords and list them by various options. Follow the Commands' instructions and you won't face any problems. **Happy Encryption!**