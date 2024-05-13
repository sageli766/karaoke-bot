import pyautogui
import time
from damvision import click_button, Button, extract_hit_list, search_loading, no_results, on_reserve_page
from loguru import logger
import pyperclip

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
    click_button(Button.SEARCH_KEYWORD)
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

def search_keyword(keyword, **kwargs):

    logger.info("performing keyword search for: " + keyword)

    pyperclip.copy(keyword)

    if kwargs:
        time.sleep(kwargs['delay'])
    click_button(Button.SEARCH_KEYWORD)
    time.sleep(0.1)
    pyautogui.keyDown('ctrlleft')
    pyautogui.keyDown('v')
    pyautogui.keyUp('v')
    pyautogui.keyUp('ctrlleft')
    
    click_button(Button.SEARCH)
    click_button(Button.MOUSE_RESET)
    
    while search_loading(): time.sleep(0.5)
    if no_results(): 
        parse_instructions([('enter', 0.5)])
        click_button(Button.TOP)
        return None, None
    return extract_hit_list()

def scroll_down_update(**kwargs):

    logger.info("scrolling down and updating hit list.")

    if kwargs:
        time.sleep(kwargs['delay'])
    parse_instructions([
                        ('d', 0), 
                        ('d', 0), 
                        ('d', 0), 
                        ('d', 0), 
                        ('d', 0), 
                        ('d', 0), 
                        ('d', 0), 
                        ('d', 0), 
                        ('d', 0),
                        ('u', 0), 
                        ('u', 0), 
                        ('u', 0), 
                        ('u', 0), 
                        ]) #TODO find a way to not get messed up by loading buffer around 30 results in using cv2
    return extract_hit_list()

def scroll_up_update(**kwargs):

    logger.info("scrolling up and updating hit list.")

    if kwargs:
        time.sleep(kwargs['delay'])
    parse_instructions([
                        ('u', 0), 
                        ('u', 0), 
                        ('u', 0), 
                        ('u', 0), 
                        ('u', 0)
                        ])
    return extract_hit_list()

def select_and_queue(number, **kwargs):

    number -= 1

    if kwargs:
        time.sleep(kwargs['delay'])

    for _ in range(number):
        parse_instructions([('d', 0)])

    parse_instructions([('enter', 0)])
    while not on_reserve_page():
        time.sleep(0.5)
    parse_instructions([('enter', 0), ('enter', 0)])
    time.sleep(1)
    click_button(Button.TOP)

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