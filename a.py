import pyautogui
import time
while True:
    x, y = pyautogui.position()
    px = pyautogui.pixel(x, y)
    print(px)
    time.sleep(1)