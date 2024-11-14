

def welcome():
    print("sukipass - a simple password manager")

def view_password():
    print("")
    
def add_password():
    nama_password = input("Masukkan nama Password")
    isi_password = input("Masukkan isi Password")
    
def change_password():
    print("")
    
def select_menu():
    input_menu = input("Silahkan pilih menu: ")
    match input_menu:
        case "1":
            view_password()
        case "2":
            add_password()
        case "3":
            change_password()
        case _:
            print("Kamu tidak memilih dengan benar :(")
            
def main():
    welcome()
    select_menu()

main()
