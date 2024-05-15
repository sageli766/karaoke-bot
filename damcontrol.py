import pyautogui
import asyncio
import time
from damvision import search_loading, on_reserve_page
from loguru import logger
import pyperclip
from enum import Enum
import scaling

class Button(Enum):
    SKIP = 539, 866
    PAUSE = 657, 864 # gotta figure out how this button actually works in the app, appears greyed out all the time
    RESTART = 771, 863
    RESTART_CONFIRM = 584, 553
    KEYDOWN = 895, 861
    KEYUP = 1008, 865
    BACK = 1124, 860
    TOP = 1238, 864
    FULLSCREEN = 1353, 859

    SEARCH_KEYWORD = 980, 256
    SEARCH_SONGNAME = 1172, 255
    SEARCH_ARTISTNAME = 1354, 254
    # SEARCH_NEWSONGS = 1370, 620
    # SEARCH_TOPCHART = 1630, 620

    SUBMIT_SEARCH = 1092, 764

    RESERVE = 1440, 750

    MOUSE_RESET = 72, 52

    GRADING_START = 547, 681

    KEY_CHANGE = 1009, 631


def click_button(button):
    """
    Click on a button. pass in damvision.Button enums.
    """
    x, y = button.value
    pyautogui.moveTo(scaling.scale_xy_offset(x, y))
    pyautogui.mouseDown()
    pyautogui.mouseUp()

    logger.debug(str(button) + " clicked")

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

async def search_keyword_and_reserve(keyword, key):
    logger.info("reserving first keyword search result for: " + keyword)

    pyperclip.copy(keyword)

    click_button(Button.SEARCH_KEYWORD)
    await asyncio.sleep(0.1)
    pyautogui.keyDown('ctrlleft')
    pyautogui.keyDown('v')
    pyautogui.keyUp('v')
    pyautogui.keyUp('ctrlleft')
    
    click_button(Button.SUBMIT_SEARCH)
    click_button(Button.MOUSE_RESET)
    
    while search_loading(): 
        await asyncio.sleep(0.5)
    
    parse_instructions([('enter', 0), ('enter', 0)])
    while not on_reserve_page():
        await asyncio.sleep(0.5)
    await change_key(key)
    click_button(Button.RESERVE)
    await asyncio.sleep(1.5)
    click_button(Button.TOP)

async def change_key(key):
    direction = key[0]
    amount = int(key[1])
    if amount == 0: return
    logger.info("changing key by: " + key)

    click_button(Button.KEY_CHANGE)
    for _ in range(amount):
        if direction == "+":
            up()
        else: 
            down()
    parse_instructions([('enter', 0)])