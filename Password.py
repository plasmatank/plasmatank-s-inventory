import string
import random
import keyboard
import time
import threading
word = "This a test."
outside = ""

def output():
    while True:
        if keyboard.is_pressed("Ctrl"):
            print(f"\r{outside}{random.choice(string.ascii_letters + string.digits)}", end="")
            time.sleep(0.01)
            if outside == word:
                print(f"\r{outside}", end="")
                break

def plus():
    for i in word:
        keyboard.wait("Ctrl")
        time.sleep(0.8)
        globals()["outside"] += i


a = threading.Thread(target=output)
b = threading.Thread(target=plus)
a.start()
b.start()