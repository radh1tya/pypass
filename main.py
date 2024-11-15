import string
import random
import os
import json

def xor_encryption(text, key):
    encrypted_text = ""
    for i in range(len(text)):
        encrypted_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return encrypted_text

def master_register():
    master_register_password = input("register password:")
    master_register_salt = ''.join(random.choices(string.ascii_letters, k=7))

    test_string = "test_string"
    encrypted_test_string = xor_encryption(test_string, master_register_password + master_register_salt)
    
    to_save = {
        "master_salt" : master_register_salt,
        "test_string" : encrypted_test_string,
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
    else:
        print("Login gagal. Password salah.")
    
def checker(password):
    with open('./data/credentials.json') as f:
        data = json.load(f)
    salt = data.get('master_salt')
    encrypted_test_string = data.get('test_string')
    
    decrypted_test = xor_encryption(encrypted_test_string, password + salt)
    
    return decrypted_test == "test_string"

def main():
    check_login()
    
if __name__ == "__main__":
    main()
