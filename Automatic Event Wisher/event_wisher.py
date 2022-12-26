import os
import shutil
import smtplib
import time
from datetime import datetime
from plyer import notification as nt
import pandas as pd
from email.message import EmailMessage
import imghdr
import pyrebase
from pathlib import Path
from config import config

time.sleep(10)

image_downloads_path = os.path.join(Path.home(), "Downloads", "AEW_images/")
start = pyrebase.initialize_app(config)

try:
    storage = start.storage()
    rdb = start.database()
except:
    nt.notify(
        title="Alert!",
        message="Can't use the app because you are offline!",
        timeout=10
        )
    quit()

files = storage.list_files()
data = rdb.get()
data = dict(data.val())

my_name = data["data"]["credentials"][0]
my_name_in_images = my_name.split()[0].lower()
my_email = data["data"]["credentials"][1]
my_password = data["data"]["credentials"][2]


def send_mail(msg):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(my_email, my_password)
    server.send_message(msg)
    server.close()

today = int(datetime.now().strftime("%d%m"))
current_day = int(datetime.now().strftime("%d"))
current_month = int(datetime.now().strftime("%m"))
current_year = int(datetime.now().strftime("%Y"))

original_df = pd.DataFrame(data)
df = pd.DataFrame(original_df["data"]["details"])
for i, j in df.iterrows():
    event_date = int(j['Date'])
    event_month = int(str(j['Date'])[-2:])
    event_day = int(str(j['Date'])[0:-2])
    event_year = int(j['Year'])

    if today == event_date and current_year == event_year:
        nt.notify(
            title=j['Name'] + "'s " + j['Event'] + "!",
            message=j['Event'] + " wish sent!",
            timeout=10
        )

        emails = j['Email'].split(',')
        for email in emails:
            msg = EmailMessage()
            msg['Subject'] = "Happy " + j['Event'] + " " + j['Name'] + "!!"
            msg['From'] = my_name
            msg['To'] = email
            msg.set_content(f"{j['Message']}\n\n{my_name}")

            if not os.path.isdir(image_downloads_path):
                os.mkdir(image_downloads_path)
            counter = 1
            for file in files:
                if j["Event"] == "Birthday":
                    if j["Name"].lower() in file.name.lower() and my_name_in_images in file.name.lower():
                        file.download_to_filename(
                            image_downloads_path + file.name)
                        with open(image_downloads_path + file.name, "rb") as f:
                            image_data = f.read()
                            image_type = imghdr.what(f.name)
                        msg.add_attachment(
                            image_data, maintype="image", subtype=image_type, filename=f"memory{counter}")
                        counter += 1
                elif j["Event"] == "Anniversary":
                    if j["Name"].lower() in file.name.lower() and my_name_in_images not in file.name.lower():
                        file.download_to_filename(
                            image_downloads_path + file.name)
                        with open(image_downloads_path + file.name, "rb") as f:
                            image_data = f.read()
                            image_type = imghdr.what(f.name)
                        msg.add_attachment(
                            image_data, maintype="image", subtype=image_type, filename=f"memory{counter}")
                        counter += 1
            send_mail(msg)
            data["data"]["details"]["Year"][i] += 1
            rdb.update(data)

    elif current_month == event_month and current_day > event_day and current_year == event_year:
        data["data"]["details"]["Year"][i] += 1
        rdb.update(data)

    elif current_month > event_month and current_year == event_year:
        data["data"]["details"]["Year"][i] += 1
        rdb.update(data)

    elif current_month < event_month and current_year > event_year:
        data["data"]["details"]["Year"][i] = current_year
        rdb.update(data)

    elif current_month == event_month and current_day < event_day and current_year > event_year:
        data["data"]["details"]["Year"][i] = current_year
        rdb.update(data)

    elif current_month == event_month and current_day > event_day and current_year > event_year:
        data["data"]["details"]["Year"][i] = current_year + 1
        rdb.update(data)

    elif today == event_date and current_year > event_year:
        nt.notify(
            title=j['Name'] + "'s " + j['Event'] + "!",
            message=j['Event'] + " wish sent!",
            timeout=10
        )

        emails = j['Email'].split(',')
        for email in emails:
            msg = EmailMessage()
            msg['Subject'] = "Happy " + j['Event'] + " " + j['Name'] + "!!"
            msg['From'] = my_name
            msg['To'] = email
            msg.set_content(f"{j['Message']}\n\n{my_name}")

            if not os.path.isdir(image_downloads_path):
                os.mkdir(image_downloads_path)
            counter = 1
            for file in files:
                if j["Event"] == "Birthday":
                    if j["Name"].lower() in file.name.lower() and my_name_in_images in file.name.lower():
                        file.download_to_filename(
                            image_downloads_path + file.name)
                        with open(image_downloads_path + file.name, "rb") as f:
                            image_data = f.read()
                            image_type = imghdr.what(f.name)
                        msg.add_attachment(
                            image_data, maintype="image", subtype=image_type, filename=f"memory{counter}")
                    counter += 1
                elif j["Event"] == "Anniversary":
                    if j["Name"].lower() in file.name.lower() and my_name_in_images not in file.name.lower():
                        file.download_to_filename(
                            image_downloads_path + file.name)
                        with open(image_downloads_path + file.name, "rb") as f:
                            image_data = f.read()
                            image_type = imghdr.what(f.name)
                        msg.add_attachment(
                            image_data, maintype="image", subtype=image_type, filename=f"memory{counter}")
                    counter += 1
            send_mail(msg)
            data["data"]["details"]["Year"][i] = current_year + 1
            rdb.update(data)
    continue

if os.path.isdir(image_downloads_path):
    shutil.rmtree(image_downloads_path)
