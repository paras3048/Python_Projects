# Secure Password Manager

A local command-line password manager built with Python.

The application allows users to securely store website credentials inside an encrypted local vault protected by a master password.

The project uses PBKDF2 for deriving an encryption key from the master password and Fernet symmetric encryption for protecting the stored credentials.

No external data, API, database server, or internet connection is required.

## Features

* Master password protection
* Encrypted local password vault
* Add website credentials
* Search saved credentials
* List saved accounts
* Delete credentials
* Secure password generation
* Password strength checking
* Persistent encrypted storage
* Three failed-login attempts before closing

## Technologies Used

* Python
* Cryptography
* JSON
* PBKDF2-HMAC
* Fernet
* `secrets`
* `getpass`

## Project Structure

```text
secure-password-manager/
│
├── main.py
├── requirements.txt
├── README.md
├── vault.dat       # Created automatically
└── salt.dat        # Created automatically
```

`vault.dat` and `salt.dat` are created automatically when the application is initialized.

## Installation

Make sure Python is installed.

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the required library:

```bash
pip install -r requirements.txt
```

## Running the Project

Run:

```bash
python main.py
```

If this is the first time running the application, you will be asked to create a master password.

```text
============================================================
CREATE PASSWORD VAULT
============================================================

Create master password:
Confirm master password:

Vault created successfully.
```

The master password must contain at least 8 characters.

## Unlocking the Vault

On subsequent launches:

```text
============================================================
UNLOCK PASSWORD VAULT
============================================================

Master password:
```

The password is entered using `getpass`, so it is not displayed in the terminal.

If the password is incorrect, the application allows three attempts.

## Main Menu

After successfully unlocking the vault:

```text
============================================================
           SECURE PASSWORD MANAGER
============================================================
1. Add Credential
2. List Credentials
3. Search Credentials
4. Delete Credential
5. Generate Password
6. Check Password Strength
7. Lock & Exit
============================================================
```

## Adding Credentials

Select:

```text
1. Add Credential
```

Enter:

```text
Website / Service: Gmail
Username / Email: example@gmail.com
```

You can either enter an existing password or generate a secure password.

### Generate a Password

Select:

```text
2. Generate secure password
```

Then choose a length:

```text
Password length (minimum 8): 20
```

The application generates a password containing a mixture of:

* Uppercase letters
* Lowercase letters
* Numbers
* Special characters

The Python `secrets` module is used instead of the regular `random` module because `secrets` is designed for security-sensitive random values.

## Searching Credentials

Select:

```text
3. Search Credentials
```

Search using a website or username.

Example:

```text
Search website or username: gmail
```

The application displays the matching credential.

```text
============================================================
SEARCH RESULTS
============================================================

Website : Gmail
Username: example@gmail.com
Password: ***************
Notes   : Personal account
```

## Password Strength Checker

Select:

```text
6. Check Password Strength
```

The application evaluates characteristics such as:

* Length
* Uppercase characters
* Lowercase characters
* Numbers
* Special characters

It returns:

```text
Password strength: Strong
```

This is a basic educational strength estimator and should not be treated as a professional password-strength library.

## Encryption Architecture

The application does not store the master password directly.

Instead, the process is:

```text
Master Password
       ↓
PBKDF2-HMAC-SHA256
       ↓
Derived Encryption Key
       ↓
Fernet
       ↓
Encrypted Vault
```

A random salt is generated when the vault is created.

The salt is stored separately in:

```text
salt.dat
```

The encrypted credentials are stored in:

```text
vault.dat
```

## Why PBKDF2?

PBKDF2 makes it computationally expensive to repeatedly guess a master password.

The project uses:

```text
Algorithm: SHA-256
Iterations: 600,000
Key Length: 32 bytes
```

The derived key is then encoded into a format usable by Fernet.

## Why Fernet?

Fernet provides authenticated symmetric encryption.

The same derived key is used to encrypt and decrypt the vault.

The stored file therefore does not contain the credentials as readable JSON.

Conceptually:

```text
Readable Credentials
       ↓
JSON
       ↓
Fernet Encryption
       ↓
Encrypted Binary Data
       ↓
vault.dat
```

## Data Stored in the Vault

Before encryption, the vault internally has a structure similar to:

```json
{
    "credentials": [
        {
            "website": "Gmail",
            "username": "example@gmail.com",
            "password": "ExamplePassword123!",
            "notes": "Personal account"
        }
    ]
}
```

This structure is encrypted before being written to disk.

## Important Security Considerations

This project is intended for learning.

It is **not a replacement for established password managers**.

Important limitations include:

* The master password cannot be recovered if forgotten.
* The application does not implement secure memory wiping.
* It does not protect against malware already running on the computer.
* It does not use hardware-backed security.
* It does not synchronize across devices.
* The password strength checker is intentionally basic.
* Anyone who obtains the master password can unlock the vault.

For a real password manager, many additional security considerations would be required.

## Program Workflow

```text
First Run
   ↓
Create Master Password
   ↓
Generate Random Salt
   ↓
Derive Encryption Key
   ↓
Create Encrypted Vault

Later Runs
   ↓
Enter Master Password
   ↓
Read Salt
   ↓
Derive Same Key
   ↓
Decrypt Vault
   ↓
Use Credentials
   ↓
Encrypt Again
   ↓
Save Vault
```

## Python Concepts Practiced

This project introduces:

* File handling
* JSON serialization
* Encryption
* Key derivation
* Hash functions
* Secure random generation
* Password handling
* `getpass`
* Exception handling
* Dictionaries
* Lists
* Functions
* Local persistent storage
* Security-oriented programming

## Learning Objective

The objective is to understand the difference between:

```text
Encoding
Hashing
Encryption
```

The project primarily uses **key derivation + encryption**.

The master password is used to derive an encryption key, while the actual credentials are encrypted and stored locally.

## Possible Improvements

After completing the basic version, the project could be extended with:

* Password history
* Credential editing
* Username/password copying to clipboard
* Auto-lock after inactivity
* Login attempt delay
* Password expiration reminders
* Search by category
* Credential tags
* Secure password strength scoring
* Import/export functionality
* Automatic encrypted backups
* Hardware security key support
* GUI using Tkinter
* SQLite-based encrypted storage