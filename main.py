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
    master_xor_password = xor_encryption(master_register_password,master_register_salt)
    return master_xor_password

def check_login():
    if not os.path.isfile('./data/credentials.json'):
        master_register()
        # membuat credentials.json kalau belum ada :)
        inside = {
            "master_salt" : "",
            "users": []
        }
        json_object = json.dumps(inside, indent=1)
        with open('./data/credentials.json', 'w') as outfile:
            outfile.write(json_object)
    else:
        login()
        
def login():
    password = input("password:")
    checker()
    
def checker():
    with open('./data/credentials.json') as f:
        data = json.load(f)
    salt = data.get('master_salt')
    return salt

def main():
    check_login()
    
