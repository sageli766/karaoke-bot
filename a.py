import pyautogui
import time
import scaling
while True:
    x, y = pyautogui.position()
    x1, y1 = scaling.get_window_pos()

    x = x - x1
    y = y - y1

    #x, y = scaling.scale_xy_offset(193,1070)

    #pyautogui.moveTo(x, y)

    px = pyautogui.pixel(x, y)
    print(x, y)
    #print(px)
    time.sleep(1)