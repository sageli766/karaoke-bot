import pyautogui
import time

import pykakasi

kks = pykakasi.kakasi()
raw_input = '点描の唄'
result = kks.convert(raw_input)
romaji_input = ''
for item in result:
    romaji_input += item['hepburn']

def queue(song):
    time.sleep(3)
    # pyautogui.moveTo(1490, 180)

    # pyautogui.mouseDown()
    # pyautogui.mouseUp()

    # time.sleep(1)

    pyautogui.moveTo(1490, 360)

    pyautogui.keyDown('enter')
    pyautogui.keyUp('enter')

    pyautogui.keyDown('enter')
    pyautogui.keyUp('enter')

    pyautogui.typewrite(f'{song}')

    pyautogui.keyDown('enter')
    pyautogui.keyUp('enter')

    pyautogui.moveTo(1490, 430)

    time.sleep(3)

    pyautogui.mouseDown()
    pyautogui.mouseUp()

    time.sleep(1)

    pyautogui.mouseDown()
    pyautogui.mouseUp()

    time.sleep(3)

    pyautogui.moveTo(1690, 830)

    pyautogui.mouseDown()
    pyautogui.mouseUp()

queue(romaji_input)