import pyautogui
import time
import damcontrol
# import scaling
# while True:
#     x, y = pyautogui.position()
#     x1, y1 = scaling.get_window_pos()

#     x = x - x1
#     y = y - y1

#     #x, y = scaling.scale_xy_offset(193,1070)

#     #pyautogui.moveTo(x, y)

#     px = pyautogui.pixel(x, y)
#     print(x, y)
#     #print(px)
#     time.sleep(1)

import pynput

# Disable mouse and keyboard events
mouse_listener = pynput.mouse.Listener(on_move=lambda x, y: None)
mouse_listener.start()
keyboard_listener = pynput.keyboard.Listener(suppress=True)
keyboard_listener.start()

pyautogui.moveTo(500,500)
mouse_listener.stop()
pyautogui.mouseDown()
pyautogui.mouseUp()
mouse_listener = pynput.mouse.Listener(suppress=True)
mouse_listener.start()
time.sleep(2)


# Enable mouse and keyboard events
mouse_listener.stop()
keyboard_listener.stop()