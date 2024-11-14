import string
import random

def generate_key():
    panjang_kunci = int(input("Tentukan Panjang Kunci:\n"))
    kunci = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=panjang_kunci))
    print(str(kunci))
    
def enkripsuki(isi_password):
    generate_key()
    
def welcome():
    print("sukipass - a simple password manager\n")

def view_password():
    print("")
    
def add_password():
    nama_password = input("Masukkan nama Password\n")
    isi_password = input("Masukkan isi Password\n")
def change_password():
    print("")
    
def select_menu():
    input_menu = input("Silahkan pilih menu: \n")
    match input_menu:
        case "1":
            view_password()
        case "2":
            add_password()
        case "3":
            change_password()
        case "4":
            generate_key()
        case _:
            print("Kamu tidak memilih dengan benar :(")
            
def main():
    welcome()
    select_menu()

main()
