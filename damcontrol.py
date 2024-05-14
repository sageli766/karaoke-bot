import pyautogui
import asyncio
import time
from damvision import search_loading, on_reserve_page
from loguru import logger
import pyperclip
from enum import Enum
import scaling

class Button(Enum):
    SKIP = 730, 1200
    PAUSE = 890, 1200 # gotta figure out how this button actually works in the app, appears greyed out all the time
    RESTART = 1050, 1200
    RESTART_CONFIRM = 800, 770
    KEYDOWN = 1210, 1200
    KEYUP = 1370, 1200
    BACK = 1530, 1200
    TOP = 1690, 1200
    FULLSCREEN = 1950, 1200

    SEARCH_KEYWORD = 1370, 350
    SEARCH_SONGNAME = 1630, 350
    SEARCH_ARTISTNAME = 1890, 350
    SEARCH_NEWSONGS = 1370, 620
    SEARCH_TOPCHART = 1630, 620

    SUBMIT_SEARCH = 1530, 1060

    RESERVE = 2000, 1050

    MOUSE_RESET = 100, 100

    GRADING_START = 765, 950


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

async def search_keyword_and_reserve(keyword):
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
    parse_instructions([('enter', 0)])
    await asyncio.sleep(1.5)
    click_button(Button.TOP)