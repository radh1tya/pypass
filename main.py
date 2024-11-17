import string
import random
import os
import json
import sys

sys.tracebacklimit = 0

def xor_encryption(text, key):
    encrypted_text = ""
    for i in range(len(text)):
        encrypted_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return encrypted_text

def master_register():
    master_register_password = input("register password:")
    master_register_salt = ''.join(random.choices(string.ascii_letters, k=7))

    etc = "your-heart-is-something-new"
    encrypted_test_string = xor_encryption(etc, master_register_password + master_register_salt)
    
    to_save = {
        "master_salt" : master_register_salt,
        "etc" : encrypted_test_string,
        "users": []
    }
    
    return to_save

def check_login():
    if not os.path.isfile('./data/credentials.json'):
        data_to_save = master_register()
        json_object = json.dumps(data_to_save, indent=1)
        with open('./data/credentials.json', 'w') as outfile:
            outfile.write(json_object)
    else:
        login()
        
def login():
    password = input("password:")
    if checker(password):
        print("Login berhasil!")
        dashboard()
    else:
        print("Login gagal. Password salah.")
    
def checker(password):
    with open('./data/credentials.json') as f:
        data = json.load(f)
    salt = data.get('master_salt')
    encrypted_test_string = data.get('etc')
    
    decrypted_test = xor_encryption(encrypted_test_string, password + salt)
    
    return decrypted_test == 'your-heart-is-something-new'

def dashboard():
    os.system('clear')
    print("Welcome to the Pypass!")
    print("You are now logged in as user " + os.getlogin())
    print("*** Ini masih percobaan ***")
    shell()
    
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
            print("e - edit password")
            print("s - system setting")
            print("h - help")
            print("q - quit")
        elif command == 'q':
            print("bye :(")
            break
        
            
def add_password():
    database_username = input("username: ")
    database_password = input("password: ")
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
            print(f"{index}. {item['username']} " + "note: " + f"{item['note']}")
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
