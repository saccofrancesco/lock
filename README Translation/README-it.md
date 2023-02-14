# Cryptographied Password Manager
Cryptographied Password Manager è uno strumento per l'archiviazione di password crittografate sul tuo computer locale.

## Set Up

### Compilare da Te
Scarica la cartella ZIP o clona il repository con:
```
clone di git https://github.com/TonicStark/cryptographied-password-manager.git
```

Quindi installa le dipendenze in un virtualenv, puoi crearne una tramite `python -m venv <nome del virtualenv>`, con:
```
pip install -r requisiti.txt
```
In *virtualenv*, esegui il seguente comando:
```
pyinstaller --onefile .\main.py
```
questo **costruirà** il file `main.py`, come un **singolo** *eseguibile*.
Quando finisci il processo di compilazione, dovresti avere un *repo* come questo:
```
.
└── cryptographied-password-manager/
    ├── build
    ├── components
    ├── dist/
    │ └── password.exe
    ├── README Translation
    ├── venv
    ├── .gitignore
    ├── main.py
    ├── README.md
    └── requirements.txt
```
All'interno di `dist/` dovresti avere un **file**, `passwords.exe` che puoi **eseguire** come un singolo programma, senza dover *attivare* il *virtualenv* ogni volta.

Per usarlo in **ogni** percorso del tuo sistema, devi aggiungere la cartella `.\cryptographied-password-manager\dist\` al tuo *Percorso computer*: [qui](https://chlee.co /how-to-setup-environment-variables-for-windows-mac-and-linux/) c'è una **guida** su come farlo.

## Scarica (solo Windows)
Altrimenti, puoi *scaricare* nella sezione **Release**, il file *compilato*, pronto per essere aggiunto al tuo *Percorso di sistema* per **usarlo!**

## Personalizzazione
Quando avvii lo script per la **PRIMA VOLTA**, scegli una **Password** da utilizzare come **_Master Password_** e **ricordala**. **OGNI volta** che vuoi **Accedere** utilizzalo e non cambiarlo **MAI**. La password principale viene utilizzata per **crittografare** le password e anche per **decrittografarle**. **_Non scriverla nel file o condividerlo con nessuno._** Ricordalo solo, inseriscilo e il programma otterrà una chiave per crittografare e decrittografare le tue password.

# Avvia il programma
Ora devi solo avviare il programma e avrai una bella interfaccia a riga di comando per archiviare, aggiornare ed eliminare le tue password. Puoi anche cercare le tue password ed elencarle in base a varie opzioni. Segui le istruzioni dei comandi e non avrai problemi. **Buona crittografia!**