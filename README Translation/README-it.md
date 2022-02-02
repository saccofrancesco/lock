# Gestore Password Crittografate
Cryptographied Password Manager è uno strumento per la memorizzazione di password crittografate nel tuo computer locale.

## Set Up
Scarica la cartella ZIP o clona il repository con:
```
git clone https://github.com/TonicStark/Cryptographied-Password-Manager.git
```

Quindi installa le dipendenze in un virtualenv, puoi crearne uno tramite `python -m venv <name of the virtualenv>`, con:
```
pip install -r requirments.txt
```

Ora devi eseguire il file `keys.py` e poi **ELIMINARLO**. Questo file popolerà i file `public_key.pem`, `private_key.pem` e `pwd_hash.pem` con del testo personalizzato. I primi due sono le tue **Chiavi Pubblica e Privata**; il terzo è la password che hai inserito, passata attraverso un HASH.

Il file `public_key.pem` può essere pubblico, quindi puoi tenerlo in questa cartella. Il `private_key.pem` non deve essere pubblico. **NON RENDERLO PUBBLICO** perché questo è l'unico modo che hai per decifrare le TUE password. È l'unico modo per invertire il processo.

Se provi ad accedere al database in altri modi, puoi vedere come le password siano archiviate in modo crittografato.

## Personalizzazione
Ora copia il file `private_key.pem` e incollalo in una cartella difficile da trovare, magari una cartella nel tuo Utente o qualcos'altro. Copia il percorso del file, ad esempio:

![esempio di percorso](img/percorso.png)

In questo caso specifico, il percorso sarà `C:\Users\franc\KEYS\private_key.pem`. Scrivi questo da qualche parte perché avremo bisogno di questo più avanti nella configurazione. Elimina la copia del file `private_key.pem` da questa cartella.

Ora apri il file `pwd_hash.pem`, copia la versione con hash della password che hai inserito e scrivila da qualche parte come la chiave privata.

Ora abbiamo 2 varianti: se sei su Windows o su un sistema Unix (Linux o Mac).

### Windows
Passate a `Pannello di controllo > Sistema e sicurezza > Sistema > Impostazioni di sistema avanzate`. Ora in Impostazioni di sistema avanzate, fai clic su "Variabili d'Ambiente".
Qui possiamo aggiungere nuove variabili utente e nuove variabili di sistema. Aggiungeremo le variabili utente facendo clic su "Nuovo" sotto le variabili utente.

Nella nuova finestra, puoi aggiungere "Nome variabile" e "Valore variabile" e fare clic su OK.

Ora prendi il percorso del file `private_key.pem` e salvalo come **PRIVATE_KEY**, in questo modo:

![key_storing_example](img/private_key.png)

La stessa cosa, devi fare ora con l'hash. Prendilo e archivialo in una variabile d'ambiente chiamata **PASSWORD_HASH**, in questo modo:

![password_hash_example](img/pwd_hash.png)

### Linux o Mac
Per impostare password o chiavi segrete nelle variabili d'ambiente su Linux (e Mac) devi modificare il file `.bash_profile` che si trova nella tua home directory. Devi aprire il terminale e poi, andare nella directory `home`.

Ora, apri il file `.bash_profile` in qualsiasi editor di testo a tua scelta, ad esempio con VS Code:
```
code .bash_profile
```
Dobbiamo aggiungere la nostra variabile di ambiente in questo file. Per questo aggiungi il seguente contenuto nella parte superiore del file:
```bash
export PRIVATE_KEY="Percorso del file private_key.pem"
export PASSWORD_HASH="L'Hash della password"
```

Ora, per caricare le nuove variabili di ambiente nella sessione della shell corrente, usa il comando source:
```
source .bash_profile
```

## Libera la Cartella
Se hai seguito tutti i passaggi precedenti e capisci come funziona questo programma, puoi anche pulire la tua cartella clonata, in questo modo:

![cleaned_folder_example](img/cleaned_folder.png)

# Avvia il Programma
Ora devi solo avviare il programma e avrai una bella interfaccia a riga di comando per archiviare, aggiornare ed eliminare le tue password. Puoi anche cercare le tue password ed elencarle in base a varie Opzioni. Segui le istruzioni dei comandi e non avrai problemi. **Buona Crittografazione!**