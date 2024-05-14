import pyautogui
import time
import scaling
while True:
    x, y = pyautogui.position()
    x1, y1 = scaling.get_window_pos()

    x = x - x1
    y = y - y1

    # px = pyautogui.pixel(x, y)
    print(x, y)
    time.sleep(1)