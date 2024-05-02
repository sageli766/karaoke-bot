import pyautogui
import time
import pykakasi

def to_romaji(song: str) -> str:
    kks = pykakasi.kakasi()
    raw_input = song
    result = kks.convert(raw_input)
    romaji_output = ''
    for item in result:
        romaji_output += item['hepburn']
    return romaji_output

def parse_instructions(instructions):
    def enter():
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter')
    def right():
        pyautogui.keyDown('right')
        pyautogui.keyUp('right')
    def left():
        pyautogui.keyDown('left')
        pyautogui.keyUp('left')
    def down():
        pyautogui.keyDown('down')
        pyautogui.keyUp('down')
    def up():
        pyautogui.keyDown('up')
        pyautogui.keyUp('up')

    for action, delay in instructions:
        if action == 'l':
            left()
        elif action == 'r':
            right()
        elif action == 'u':
            up()
        elif action == 'd':
            down()
        elif action == 'enter':
            enter()
        time.sleep(0.2)

def queue(song, **kwargs):
    if kwargs:
        time.sleep(kwargs['delay'])

    parse_instructions(['r', 'enter'])
    pyautogui.typewrite(song)
    parse_instructions(['enter', 'enter', 'd', 'd', 'r', 'r', 'r'])
    enter()
    time.sleep(0.5)
    enter()
    time.sleep(0.5)
    enter()

    # pyautogui.moveTo(1490, 360)
    #
    # pyautogui.keyDown('enter')
    # pyautogui.keyUp('enter')
    #
    # pyautogui.keyDown('enter')
    # pyautogui.keyUp('enter')
    #
    # pyautogui.typewrite(f'{song}')
    #
    # pyautogui.keyDown('enter')
    # pyautogui.keyUp('enter')
    #
    # pyautogui.moveTo(1490, 430)
    #
    # time.sleep(3)
    #
    # pyautogui.mouseDown()
    # pyautogui.mouseUp()
    #
    # time.sleep(1)
    #
    # pyautogui.mouseDown()
    # pyautogui.mouseUp()
    #
    # time.sleep(3)
    #
    # pyautogui.moveTo(1690, 830)
    #
    # pyautogui.mouseDown()
    # pyautogui.mouseUp()

# queue(romaji_output)