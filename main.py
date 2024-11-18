import getpass
import signal
import string
import random
import os
import json
import sys

# :(
from cryptography.fernet import Fernet

sys.tracebacklimit = 0

def signal_handler(signum, frame):
    encrypt_credentials()
    sys.exit(0)

def generate_key():
    key = Fernet.generate_key()
    with open('./data/shalt-thou-be-a-sellout.key', 'wb') as filekey:
        filekey.write(key)

def encrypt_credentials():
    with open('./data/shalt-thou-be-a-sellout.key', 'rb') as filekey:
        key = filekey.read()
    fernet = Fernet(key)
    
    with open('./data/credentials.json', 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)

    with open('./data/credentials-encrypted.json', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    os.remove('./data/credentials.json')
    
def decrypted_credentials():
    with open('./data/shalt-thou-be-a-sellout.key', 'rb') as filekey:
        key = filekey.read()
    fernet = Fernet(key)

    with open('./data/credentials-encrypted.json', 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)

    with open('./data/credentials.json', 'wb') as dec_file:
        dec_file.write(decrypted)
    os.remove('./data/credentials-encrypted.json')
    
def xor_encryption(text, key):
    encrypted_text = ""
    for i in range(len(text)):
        encrypted_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return encrypted_text

def master_register():
    directory_name = "./data/"
    os.mkdir(directory_name)
    master_register_password = getpass.getpass("register password:")
    master_register_salt = ''.join(random.choices(string.ascii_letters, k=7))

    etc = "your-heart-is-something-new"
    encrypted_test_string = xor_encryption(etc, master_register_password + master_register_salt)
    
    to_save = {
        "already_created_before": True,
        "master_salt" : master_register_salt,
        "etc" : encrypted_test_string,
        "users": []
    }

    with open('./data/credentials.json', 'w') as outfile:
        json.dump(to_save, outfile, indent=1)
    generate_key()
    encrypt_credentials()
   
def check_login():
    if not os.path.isfile('./data/credentials-encrypted.json'):
        master_register()
    else:
        decrypted_credentials()
        login()
        
def login():
    password  = getpass.getpass("password:")
    if checker(password):
        print("Login berhasil!")
        dashboard()
    else:
        print("Login gagal. Password salah.")
        encrypt_credentials()
    
def checker(password):
    with open('./data/credentials.json') as f:
        data = json.load(f)
    salt = data.get('master_salt')
    encrypted_test_string = data.get('etc')
    
    decrypted_test = xor_encryption(encrypted_test_string, password + salt)
    return decrypted_test == 'your-heart-is-something-new'

def dashboard():
    signal.signal(signal.SIGINT, signal_handler)
    try:
        os.system('clear')
        print("Welcome to the Pypass!")
        print("You are now logged in as user " + os.getlogin())
        print("*** Ini masih percobaan ***")
        shell()
    except Exception as e:
    finally:
        encrypt_credentials()
        sys.exit(0)
        
def shell():
    while True:
        sh = input("pypass> ")
        parts = sh.split()
        command = parts[0] if parts else None
        args = parts[1:] if len(parts) > 1 else []
        if command == 'a':
            add_password()
        elif command == 'l':
            list_password()
        elif command == 's':
            if args:
                index = int(args[0]) - 1
                see_password(index)
        elif command == 'h':
            print("a - add new entry")
            print("l - list password")
            print("h - help")
            print("q - quit")
        elif command == 'q':
            print("bye :(")
            break

def add_password():
    database_username = input("username: ")
    database_password = getpass.getpass("password: ")
    database_ask_note = input("note? 1 or 0: ")
    if database_ask_note == '1':
        database_note = input("note: ")
    else:
        database_note = "0"

    database_salt = ''.join(random.choices(string.ascii_letters, k=7))

    database_both_encrypted = xor_encryption(database_password,database_salt)
    
    database_to_json = {
        "username" : database_username,
        "password" : database_both_encrypted,
        "salt": database_salt,
        "note" : database_note
        }
 
    if os.path.isfile('./data/credentials.json'):
        with open('./data/credentials.json', 'r') as infile:
            existing_data = json.load(infile)
        existing_data['users'].append(database_to_json)
    else:
        existing_data = {
            "master_salt": "",
            "etc": "",
            "users": [database_to_json]
        }
    
    with open('./data/credentials.json', 'w') as outfile:
        json.dump(existing_data, outfile, indent=1)

def list_password():
    with open('./data/credentials.json', 'r') as infile:
        existing_data = json.load(infile)
    for index, item in enumerate(existing_data["users"], start=1):
        if item['note'] == '0':
            print(f"{index}. {item['username']}")
            print("---")
        else:
            print(f"{index}. {item['username']} " + "(" + f"{item['note']}" +")")
            print("---")
        
def see_password(index):
    with open('./data/credentials.json', 'r') as infile:
        existing_data = json.load(infile)
        
    if 0 <= index < len(existing_data["users"]):
        user = existing_data["users"][index]
        password = xor_encryption(user["password"], user["salt"])
        print(f"Password for {user['username']}: {password}")
        
def main():
    os.system('clear')
    check_login()
    
if __name__ == "__main__":
    main()
