from getpass import getpass
from cryptography.fernet import Fernet
import firebase_admin
from firebase_admin import db
from config import private_key, my_key


# def produce_key():
#     key = Fernet.generate_key()
#     fer = Fernet(key)
#     with open("key.key", "wb") as f:
#         f.write(key)

# def fetch_key():
#     with open("key.key", "rb") as f:
#         key = f.read()
#     return key

def create_account():
    global username
    username = input ("Please choose a unique username: ").strip()
    if "$" in username or "#" in username or "[" in username or "]" in username or "/" in username or "." in username:
        print()
        print("Master username cannot contain '$', '#', '[', ']', '/', or '.'")
        return
    elif username == "CANCEL":
        return 2
    elif username in temp_data:
        print()
        print("Sorry, an account with this username already exists!")
        return 0
    while True:
        master_pass = getpass ("Please choose the master password (Minimum 8 characters): ")
        if master_pass == "CANCEL":
            return 2
        if len(master_pass.strip()) >= 8 and master_pass != username:
            confirm_master_pass = getpass("Re-type to confirm: ")
            if confirm_master_pass == "CANCEL":
                return 2
            elif master_pass != confirm_master_pass:
                print()
                print("Passwords don't match!")
                print()
                continue
            else:
                temp_data[username] = list([fer.encrypt(master_pass.encode()).decode(), {}])
                ref.set(temp_data)
                print()
                print("Account successfully created! Press 2 to login.")
                return 0
        elif len(master_pass.strip()) < 8:
            print()
            print("Master password should be at least 8 characters long!")
            print()
            continue
        elif master_pass == username:
            print()
            print("Master cannot be same as the username!")
            print()
            continue

def login():
    global username
    username = input ("Please enter your username: ").strip()
    if username == "CANCEL":
        return 2
    elif username not in temp_data:
        print()
        print("Sorry, an account with this username doesn't exist! Press 1 to sign up.")
        return 0
    while True:
        master_pass = getpass ("Please enter the master password: ")
        if master_pass == "CANCEL":
            return 2
        elif master_pass == str(fer.decrypt(temp_data[username][0].strip().encode()).decode()):
            print()
            print("Logged in successfully!")
            print()
            while True:
                print (
                "What would you like to do?" +"\n\n"
                "1. Add new account details" + "\n"
                "2. View all saved accounts" + "\n"
                "3. Search an account with a keyword" + "\n"
                "4. Change an account's name" + "\n"
                "5. Change an account's password" + "\n"
                "6. Delete an account's password" + "\n"
                "7. Change the master username" + "\n"
                "8. Change the master password" + "\n"
                "9. Delete your Simple Password Manager account" + "\n"
                "10. Press 'q' to logout and quit application" + "\n"
                "\nNote: Type 'CANCEL' to cancel an operation/return to the main menu\n"
                )
                choice = input("Enter a choice: ").lower()
                if choice == '1':
                    add_passwords()
                    print()
                elif choice == '2':
                    view_passwords()
                    print()
                elif choice == '3':
                    search_password()
                    print()
                elif choice == '4':
                    change_account_name()
                    print()
                elif choice == '5':
                    change_account_password()
                    print()
                elif choice == '6':
                    delete_account_password()
                    print()
                elif choice == '7':
                    change_master_username()
                    print()
                    if flag == 1:
                        return 0
                elif choice == '8':
                    change_master_password()
                    print()
                elif choice == '9':
                    if delete_your_account() == 1:
                        print("Thank you for using Simple Password Manager! Goodbye!")
                        y = input ("Press enter to QUIT...")
                        return 1
                    else:
                        continue
                elif choice == 'q':
                    print()
                    print(f"You have logged out! Goodbye {username}!")
                    y = input ("Press enter to QUIT...")
                    return 1
                else:
                    print()
                    print("Please enter a valid choice number!")
                    print()
                    continue
        else:
            print()
            print("Incorrect master password! Please try again!")
            print()
            continue

def add_passwords():
    print()
    account_name = input ("Account name/Username: ").strip()
    if "$" in account_name or "#" in account_name or "[" in account_name or "]" in account_name or "/" in account_name or "." in account_name:
        print()
        print("Account names cannot contain '$', '#', '[', ']', '/', or '.'")
        return
    elif account_name in temp_data[username][1].keys():
        print()
        print("Account already exists!")
        return
    elif account_name == "CANCEL":
        return 2
    password = getpass ("Password: ")
    if password == "CANCEL":
        return 2
    temp_data[username][1][account_name] = fer.encrypt(password.encode()).decode()
    ref.set(temp_data)
    print()
    print("Account details successfully added!")

def view_passwords():
    if bool(temp_data[username][1]):
        print("\n********************************************************")
        print(f"Here are your passwords (Total {len(temp_data[username][1])}):")
        for key, val in temp_data[username][1].items():
            print()
            print(f"Account: {key}")
            print(f"Password: {str(fer.decrypt(val.strip().encode()).decode())}")
        print("\n********************************************************")
    else:
        print()
        print("Sorry, you have not saved any passwords! Press 1 to add a password.")

def search_password():
    print()
    original_keyword = input ("Enter a keyword to search: ").strip()
    if original_keyword == "CANCEL":
        return 2
    keyword = original_keyword.lower()
    lst = []
    for key in temp_data[username][1].keys():
        if keyword in key.lower():
            lst.append(f"Account: {key}\nPassword: {str(fer.decrypt(temp_data[username][1][key].strip().encode()).decode())}")
    if len(lst) != 0:
        print("\n********************************************************")
        print(f"Here are the search results for '{original_keyword}':")
        print()
        for string in lst:
            print(string)
            print()
        print("********************************************************")
    else:
        print()
        print(f"Sorry, there is no account containing the keyword '{original_keyword}'!")

def change_account_name():
    print()
    an = input("Enter the current acccount name which is to be changed: ").strip()
    if an == "CANCEL":
        return 2
    print()
    for key in temp_data[username][1].keys():
        if an == key:
            new_an = input ("Enter the new account name: ").strip()
            if "$" in new_an or "#" in new_an or "[" in new_an or "]" in new_an or "/" in new_an or "." in new_an:
                print()
                print("Account names cannot contain '$', '#', '[', ']', '/', or '.'")
                return
            if new_an == "CANCEL":
                return 2
            temp_data[username][1][new_an] = temp_data[username][1].pop(an)
            ref.set(temp_data)
            print()
            print(f"Account name successfully changed!")
            return
    print("This account doesn't exist in the list!")

def change_account_password():
    print()
    which_account = input("Enter the exact name of the account whose password is to be changed: ")
    if which_account == "CANCEL":
        return 2
    print()
    for key in temp_data[username][1].keys():
        if key == which_account:
            while True:
                new_pass = getpass("Enter the new password for this account: ")
                if new_pass == "CANCEL":
                    return 2
                temp_data[username][1][which_account] = fer.encrypt(new_pass.encode()).decode()
                ref.set(temp_data)
                print()
                print(f"Password successfully changed for {which_account}!")
                return
    print("This account doesn't exist in the list!")

def delete_account_password():
    print()
    account_to_be_deleted = input("Enter the exact name of the account to be deleted: ")
    if account_to_be_deleted == "CANCEL":
        return 2
    print()
    if account_to_be_deleted in temp_data[username][1].keys():
        confirm = input("Are you sure? (Y/N): ")
        confirm.lower()
        if confirm == 'y':
            del(temp_data[username][1][account_to_be_deleted])
            ref.set(temp_data)
            print()
            print("Account successfully deleted!")
    else:
        print("This account doesn't exist in the list!")

def change_master_username():
    global flag
    flag = 0
    print()
    mu = input("Enter the current master username: ").strip()
    if mu == "CANCEL":
        return 2
    print()
    if mu == username:
        new_mu = input ("Enter the new master username: ").strip()
        if "$" in new_mu or "#" in new_mu or "[" in new_mu or "]" in new_mu or "/" in new_mu or "." in new_mu:
            print()
            print("Master username cannot contain '$', '#', '[', ']', '/', or '.'")
            return
        elif new_mu == "CANCEL":
            return 2
        elif new_mu == username or new_mu not in temp_data.keys():
            temp_data[new_mu] = temp_data.pop(username)
            ref.set(temp_data)
            print()
            print(f"Master username successfully changed! Please login again!", end = "")
            flag = 1
            return
    else:
        print("Incorrect master username!")

def change_master_password():
    print()
    current_mp = getpass ("Enter the current master password: ")
    if current_mp == "CANCEL":
        return 2
    if current_mp == str(fer.decrypt(temp_data[username][0].strip().encode()).decode()):
        while True:
            new_mp = getpass("Enter the new master password (Minimum 8 characters): ")
            if new_mp == "CANCEL":
                return 2
            if len(new_mp.strip()) >= 8:
                confirm_new_mp = getpass("Re-type to confirm: ")
                if confirm_new_mp == "CANCEL":
                    return 2
                elif new_mp == confirm_new_mp:
                    temp_data[username][0] = fer.encrypt(new_mp.encode()).decode()
                    ref.set(temp_data)
                    print()
                    print("Master password successfully changed!")
                    break
                else:
                    print()
                    print("Passwords don't match!")
                    print()
                    continue
            elif len(new_mp.strip()) < 8:
                print()
                print("Master password should be at least 8 characters long!")
                print()
                continue
            elif new_mp == username:
                print()
                print("Master cannot be same as the username!")
                print()
                continue
    else:
        print()
        print("Incorrect current master password!")

def delete_your_account():
    print()
    confirm_password = getpass("Type in your master password to confirm account deletion: ").strip()
    if confirm_password == "CANCEL":
        print()
        return 2
    elif confirm_password == str(fer.decrypt(temp_data[username][0].strip().encode()).decode()):
        del(temp_data[username])
        ref.set(temp_data)
        print()
        print("Account successfully deleted!")
        print()
        return 1
    else:
        print()
        print("Incorrect master password!")
        print()
        return 0

def connect_to_db():
    cred_obj = firebase_admin.credentials.Certificate(private_key)
    default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': "https://simple-password-manager-dd77a-default-rtdb.firebaseio.com/"})

    global ref
    ref = db.reference("/")

    global temp_data
    
    temp_data = ref.get()

    if not temp_data:
        temp_data = {}

def driver_code():

    # Firebase connection code
    try:
        connect_to_db()
    except:
        print("Please connect to the internet and restart the application!!!")
        x = input ("Press enter to QUIT...")
        return

    global fer
    fer = Fernet(my_key)
    print("Welcome to Simple Password Manager!!!")

    while True:
        print()
        print(
        "1. Create a new account" + "\n"
        "2. Login to an existing account" + "\n"
        "3. Press 'q' to quit application" + "\n"
        "\nNote: Type 'CANCEL' to cancel an operation/return to the main menu\n"
    )
        inp = input("Enter a choice: ").lower()
        print()
        if inp == '1':
            try:
                ca = create_account()
                if ca == 0 or ca == 2:
                    continue
            except:
                print()
                print("Please connect to the internet and restart the application!!!")
                print("Any changes made beyond this point will not be saved!!!")
        elif inp == '2':
            try:
                l = login()
                if l == 0 or l == 2:
                    continue
                else:
                    break
            except:
                print()
                print("Please connect to the internet and restart the application!!!")
                print("Any changes made beyond this point will not be saved!!!")
        elif inp == 'q':
            print("Thank you for using Simple Password Manager! Goodbye!")
            y = input ("Press enter to QUIT...")
            break
        else:
            print("Please enter a valid choice number!")
            continue

if __name__ == "__main__":
    driver_code()