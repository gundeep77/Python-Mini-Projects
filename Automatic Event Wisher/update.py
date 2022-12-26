import pyrebase
from config import config

start = pyrebase.initialize_app(config)

try:
    storage = start.storage()
    rdb = start.database()
except:
    print("Cant't use the app because you are offline!")
    exit()
data = rdb.get()
data = dict(data.val())

print("What do you want to do?\n")
print(
    "1. Add a record\n"
    "2. Add a photo\n"
    "3. Show all records\n"
    "4. Show all photos\n"
    "5. Remove a record\n"
    "6. Remove a photo\n"
    "7. Press q to quit\n"
)

def show_all_records():
    final = []
    all_details = data['data']['details']
    for i in range(len(all_details['Date'])):
        lst = []
        lst.append(i+1)
        lst.append(all_details["Date"][i])
        lst.append(all_details["Name"][i])
        lst.append(all_details["Event"][i])
        lst.append(all_details["Email"][i])
        # lst.append(all_details["Message"][i])
        lst.append(all_details["Year"][i])
        final.append(lst)
    return final

while True:
    choice = input ("Enter a choice: ")
    print()

    if choice == '1':
        name = input("Enter name: ")
        dob = int(input("Enter DOB: "))
        email = input("Enter email: ")
        event = input("Enter event: ")
        message = input("Enter message: ")
        year = int(input("Enter year: "))
        data["data"]["details"]["Name"].append(name)
        data["data"]["details"]["Date"].append(dob)
        data["data"]["details"]["Email"].append(email)
        data["data"]["details"]["Event"].append(event)
        data["data"]["details"]["Message"].append(message)
        data["data"]["details"]["Year"].append(year)
        rdb.update(data)
        print("\nRecord added successfully!")
        print()

    elif choice == '2':
        path = input("Enter the full path of the image to be uploaded: ")
        filename = path.split('/')
        list_of_images = []
        for image in storage.list_files():
            list_of_images.append(image.name.lower())
        image_name = input("\nEnter the name with which you want the image to be uploaded: ")
        if image_name.lower() not in list_of_images:
            storage.child(image_name).put(path)
            print(f"\n{image_name} added successfully!")
            print()
        else:
            print("\nAn image with the same name already exists!")
            print()

    elif choice == '3':
        for record in show_all_records():
            print(record)
        print()

    elif choice == '4':
        for image in storage.list_files():
            print(image.name)
        print()

    elif choice == '5':
        inp = int(input("Enter the record number: "))
        del(data["data"]["details"]["Name"][inp - 1])
        del(data["data"]["details"]["Date"][inp - 1])
        del(data["data"]["details"]["Email"][inp - 1])
        del(data["data"]["details"]["Event"][inp - 1])
        del(data["data"]["details"]["Message"][inp - 1])
        del(data["data"]["details"]["Year"][inp - 1])
        rdb.update(data)

        print(f"\nRecord number {inp} has been removed from database successfully!")
        print()
        
    elif choice == '6':
        image_name = input("Enter the name of the image to be removed: ")
        storage.child(image_name).delete(image_name)
        print(f"\nImage {image_name} removed from database successfully!")
        print()

    elif choice == 'q':
        print("Goodbye!!")
        x = input("Press enter to quit...")
        break

    else:
        print("Please enter a valid choice!\n")