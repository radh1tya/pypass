import string
import random
import os

def register():
    register_password = input("register password:")
    register_salt = ''.join(random.choices(string.ascii_letters, k=7))
    print("password = " + register_password)
    print("salt = " + register_salt)
    print("harap simpan baik-baik untuk decrypt :)")

    
    return register_password

def check_login():
    if not os.path.isfile('./data/credentials.json'):
        register()
    else:
        login()
        
def login():
    password = input("password:")
    return password

def authentication():
    if login() == 
    
