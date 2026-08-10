import base64
import json
import os
import secrets
import string
from pathlib import Path
from getpass import getpass

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


VAULT_FILE = Path("vault.dat")
SALT_FILE = Path("salt.dat")

ITERATIONS = 600_000


# ============================================================
# KEY DERIVATION
# ============================================================

def derive_key(password, salt):
    """
    Derive an encryption key from the master password.
    """

    password_bytes = password.encode()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS
    )

    key = kdf.derive(password_bytes)

    return base64.urlsafe_b64encode(key)


# ============================================================
# VAULT SETUP
# ============================================================

def create_vault():

    print("\n" + "=" * 60)
    print("CREATE PASSWORD VAULT")
    print("=" * 60)

    while True:

        password = getpass(
            "Create master password: "
        )

        if len(password) < 8:
            print(
                "Master password must contain "
                "at least 8 characters."
            )
            continue

        confirmation = getpass(
            "Confirm master password: "
        )

        if password != confirmation:
            print(
                "Passwords do not match."
            )
            continue

        break

    salt = os.urandom(16)

    key = derive_key(
        password,
        salt
    )

    fernet = Fernet(key)

    empty_vault = {
        "credentials": []
    }

    encrypted_data = fernet.encrypt(
        json.dumps(
            empty_vault
        ).encode()
    )

    with open(SALT_FILE, "wb") as file:
        file.write(salt)

    with open(VAULT_FILE, "wb") as file:
        file.write(encrypted_data)

    print(
        "\nVault created successfully."
    )

    return fernet, empty_vault


# ============================================================
# LOGIN
# ============================================================

def unlock_vault():

    if not VAULT_FILE.exists() or not SALT_FILE.exists():

        return create_vault()

    with open(SALT_FILE, "rb") as file:
        salt = file.read()

    print("\n" + "=" * 60)
    print("UNLOCK PASSWORD VAULT")
    print("=" * 60)

    for attempt in range(3):

        password = getpass(
            "Master password: "
        )

        try:

            key = derive_key(
                password,
                salt
            )

            fernet = Fernet(key)

            with open(VAULT_FILE, "rb") as file:
                encrypted_data = file.read()

            decrypted_data = fernet.decrypt(
                encrypted_data
            )

            vault = json.loads(
                decrypted_data.decode()
            )

            print(
                "\nVault unlocked successfully."
            )

            return fernet, vault

        except Exception:

            remaining = 2 - attempt

            if remaining > 0:
                print(
                    f"Incorrect password. "
                    f"{remaining} attempt(s) remaining."
                )

    print(
        "\nUnable to unlock vault."
    )

    return None, None


# ============================================================
# SAVE VAULT
# ============================================================

def save_vault(fernet, vault):

    data = json.dumps(
        vault,
        indent=4
    ).encode()

    encrypted_data = fernet.encrypt(
        data
    )

    with open(VAULT_FILE, "wb") as file:
        file.write(encrypted_data)


# ============================================================
# PASSWORD GENERATOR
# ============================================================

def generate_password(length=16):

    characters = (
        string.ascii_letters
        + string.digits
        + string.punctuation
    )

    while True:

        password = "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(
                c in string.punctuation
                for c in password
            )
        ):
            return password


def create_generated_password():

    print("\n" + "=" * 50)
    print("PASSWORD GENERATOR")
    print("=" * 50)

    while True:

        try:

            length = int(
                input(
                    "Password length "
                    "(minimum 8): "
                )
            )

            if length < 8:

                print(
                    "Length must be at least 8."
                )

                continue

            break

        except ValueError:

            print(
                "Please enter a valid number."
            )

    password = generate_password(
        length
    )

    print(
        f"\nGenerated password:\n{password}"
    )


# ============================================================
# ADD CREDENTIAL
# ============================================================

def add_credential(
    vault,
    fernet
):

    print("\n" + "=" * 50)
    print("ADD CREDENTIAL")
    print("=" * 50)

    website = input(
        "Website / Service: "
    ).strip()

    username = input(
        "Username / Email: "
    ).strip()

    if not website or not username:

        print(
            "Website and username "
            "cannot be empty."
        )

        return

    print("\nPassword Options")
    print("1. Enter password manually")
    print("2. Generate secure password")

    while True:

        choice = input(
            "Choose option: "
        ).strip()

        if choice in ["1", "2"]:
            break

        print("Invalid choice.")

    if choice == "1":

        password = getpass(
            "Password: "
        )

    else:

        while True:

            try:

                length = int(
                    input(
                        "Password length "
                        "(minimum 8): "
                    )
                )

                if length >= 8:
                    break

                print(
                    "Length must be at least 8."
                )

            except ValueError:

                print(
                    "Enter a valid number."
                )

        password = generate_password(
            length
        )

        print(
            f"\nGenerated password:\n{password}"
        )

    notes = input(
        "Notes (optional): "
    ).strip()

    credential = {
        "website": website,
        "username": username,
        "password": password,
        "notes": notes
    }

    vault["credentials"].append(
        credential
    )

    save_vault(
        fernet,
        vault
    )

    print(
        "\nCredential saved successfully."
    )


# ============================================================
# VIEW CREDENTIALS
# ============================================================

def list_credentials(vault):

    credentials = vault["credentials"]

    if not credentials:

        print(
            "\nNo credentials stored."
        )

        return

    print("\n" + "=" * 60)
    print("SAVED ACCOUNTS")
    print("=" * 60)

    for index, credential in enumerate(
        credentials,
        start=1
    ):

        print(
            f"{index}. "
            f"{credential['website']} "
            f"- {credential['username']}"
        )


# ============================================================
# SEARCH CREDENTIAL
# ============================================================

def search_credentials(vault):

    credentials = vault["credentials"]

    if not credentials:

        print(
            "\nNo credentials stored."
        )

        return

    search = input(
        "\nSearch website or username: "
    ).strip().lower()

    matches = []

    for credential in credentials:

        if (
            search in credential["website"].lower()
            or search in credential["username"].lower()
        ):

            matches.append(
                credential
            )

    if not matches:

        print(
            "\nNo matching credentials found."
        )

        return

    print("\n" + "=" * 60)
    print("SEARCH RESULTS")
    print("=" * 60)

    for credential in matches:

        print(
            f"\nWebsite : "
            f"{credential['website']}"
        )

        print(
            f"Username: "
            f"{credential['username']}"
        )

        print(
            f"Password: "
            f"{credential['password']}"
        )

        if credential["notes"]:

            print(
                f"Notes   : "
                f"{credential['notes']}"
            )


# ============================================================
# DELETE CREDENTIAL
# ============================================================

def delete_credential(
    vault,
    fernet
):

    credentials = vault["credentials"]

    if not credentials:

        print(
            "\nNo credentials stored."
        )

        return

    list_credentials(
        vault
    )

    while True:

        try:

            choice = int(
                input(
                    "\nEnter credential number "
                    "to delete: "
                )
            )

            if 1 <= choice <= len(credentials):
                break

            print(
                "Invalid credential number."
            )

        except ValueError:

            print(
                "Enter a valid number."
            )

    credential = credentials[
        choice - 1
    ]

    print(
        f"\nSelected: "
        f"{credential['website']}"
    )

    confirmation = input(
        "Delete this credential? (y/n): "
    ).lower()

    if confirmation != "y":

        print(
            "Deletion cancelled."
        )

        return

    credentials.pop(
        choice - 1
    )

    save_vault(
        fernet,
        vault
    )

    print(
        "\nCredential deleted."
    )


# ============================================================
# PASSWORD STRENGTH
# ============================================================

def password_strength():

    password = getpass(
        "\nEnter password to evaluate: "
    )

    score = 0

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(
        c in string.punctuation
        for c in password
    ):
        score += 1

    if score <= 2:
        strength = "Weak"

    elif score <= 4:
        strength = "Medium"

    else:
        strength = "Strong"

    print(
        f"\nPassword strength: {strength}"
    )


# ============================================================
# MENU
# ============================================================

def display_menu():

    print("\n" + "=" * 60)
    print("           SECURE PASSWORD MANAGER")
    print("=" * 60)

    print("1. Add Credential")
    print("2. List Credentials")
    print("3. Search Credentials")
    print("4. Delete Credential")
    print("5. Generate Password")
    print("6. Check Password Strength")
    print("7. Lock & Exit")

    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():

    fernet, vault = unlock_vault()

    if fernet is None:

        print(
            "\nApplication closed."
        )

        return

    while True:

        display_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            add_credential(
                vault,
                fernet
            )

        elif choice == "2":

            list_credentials(
                vault
            )

        elif choice == "3":

            search_credentials(
                vault
            )

        elif choice == "4":

            delete_credential(
                vault,
                fernet
            )

        elif choice == "5":

            create_generated_password()

        elif choice == "6":

            password_strength()

        elif choice == "7":

            print(
                "\nVault locked."
            )

            break

        else:

            print(
                "\nInvalid choice."
            )


if __name__ == "__main__":
    main()