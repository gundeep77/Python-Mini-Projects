import time
import os
from pathlib import Path
from plyer import notification as nt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PATH = "C:\Program Files (x86)\chromedriver.exe"

songs_list_path = os.path.join(Path.home(), "Desktop", "Songs List for Automated Download.txt")

if not os.path.exists(songs_list_path):
    f_temp = open(songs_list_path, 'w')
    f_temp.close()
    nt.notify(
        title = "Mp3 Songs Automatic Downloader",
        message = 'A temporary file named "Songs List for Automated Download" has been created. Please enter the songs (one in each line), save it and run the application again!',
        timeout = 15,
        app_icon = r"D:\Projects\PythonProjects\python_mini_projects\mp3_downloader(selenium)\music-note.ico"
    )
    exit()

f = open(songs_list_path, 'r')
songs = f.readlines()

if not len(songs):
    nt.notify(
        title = "Mp3 Songs Automatic Downloader",
        message = 'Songs list empty!',
        timeout = 7,
        app_icon = r"D:\Projects\PythonProjects\python_mini_projects\mp3_downloader(selenium)\music-note.ico"
    )
    exit()

driver = webdriver.Chrome(PATH)

driver.get("https://mp3quack.lol/")

for song in songs:
    driver.find_element_by_id("searchInput").clear()
    search = driver.find_element_by_id("searchInput")
    search.send_keys(song.strip())
    search.send_keys(Keys.RETURN)
    time.sleep(2)
    download = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[2]/div[2]/ul[1]/li[3]")
    download.click()
    handles = driver.window_handles
    driver.switch_to.window(handles[0])
    if len(handles) > 1:
        for i in range(1, len(handles)):
            driver.switch_to.window(handles[i])
            driver.close()    
        driver.switch_to.window(handles[0])
        download = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[2]/div[2]/ul[1]/li[3]")
        download.click()
    time.sleep(2)
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    song_link = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/div[3]/ul/li[1]")
    song_link.click()
    time.sleep(2)
    driver.switch_to.window(handles[1])
    driver.close()
    time.sleep(2)
    driver.switch_to.window(handles[0])