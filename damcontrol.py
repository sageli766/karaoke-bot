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
    
    click_button(Button.SUBMIT_SEARCH)
    click_button(Button.MOUSE_RESET)
    
    while search_loading(): time.sleep(0.5)
    if no_results(): 
        parse_instructions([('enter', 0.5)])
        click_button(Button.TOP)
        return None, None
    return extract_hit_list()

def search_keyword_and_reserve(keyword):

    logger.info("reserving first keyword search result for: " + keyword)

    pyperclip.copy(keyword)

    click_button(Button.SEARCH_KEYWORD)
    time.sleep(0.1)
    pyautogui.keyDown('ctrlleft')
    pyautogui.keyDown('v')
    pyautogui.keyUp('v')
    pyautogui.keyUp('ctrlleft')
    
    click_button(Button.SUBMIT_SEARCH)
    click_button(Button.MOUSE_RESET)
    
    while search_loading(): time.sleep(0.5)
    
    parse_instructions([('enter', 0), ('enter', 0)])
    while not on_reserve_page():
        time.sleep(0.5)
    parse_instructions([('enter', 0)])
    time.sleep(1)
    click_button(Button.TOP)

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
