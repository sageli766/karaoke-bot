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

def parse_instructions(instructions):
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
        else:
            pass
        time.sleep(delay)

def queue(song, key, **kwargs):
    if kwargs:
        time.sleep(kwargs['delay'])
    pyautogui.moveTo(1500, 200, duration=0.5)
    pyautogui.mouseDown()
    pyautogui.mouseUp()
    pyautogui.mouseDown()
    pyautogui.mouseUp()
    time.sleep(0.5)
    parse_instructions([('enter', 0.2)])
    pyautogui.typewrite(song)
    time.sleep(1)
    parse_instructions([('enter', 0.2), 
                        ('enter', 0.2), 
                        ('pass', 3),
                        ('d', 0.1), 
                        ('d', 0.1), 
                        ('r', 0.1), 
                        ('r', 0.1), 
                        ('r', 2),
                        ('enter', 2), 
                        ('enter', 3),
                        ('u', 0.1),
                        ('l', 0.1),
                        ('l', 0.1),
                        ('enter', 0)
                        ])
    
    for _ in range(abs(key)):
        if key > 0:
            up()
        elif key < 0:
            down()
        time.sleep(0.2)

    parse_instructions([('enter', 0.1),
                        ('r', 0.1),
                        ('r', 0.1),
                        ('d', 0.2),
                        ('enter', 0.2)])

    pyautogui.moveTo(610, 760, duration=0.5)
    time.sleep(2)
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.mouseUp()

def cancel():
    pyautogui.moveTo(610, 950, duration=0.5)
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.mouseUp()

def pause():
    pyautogui.moveTo(750, 950, duration=0.5)
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.mouseUp()

def restart():
    pyautogui.moveTo(900, 950, duration=0.5)
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.mouseUp()

def keyup():
    pyautogui.moveTo(1030, 950, duration=0.5)
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.mouseUp()

def keydown():
    pyautogui.moveTo(1160, 950, duration=0.5)
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.mouseUp()