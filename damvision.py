import cv2
import pyautogui
import numpy as np
from enum import Enum
from loguru import logger
import easyocr
import pytesseract
from numpy import asarray
import scaling

reader = easyocr.Reader(['ja','en'])
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # you may have to install https://github.com/UB-Mannheim/tesseract/wiki

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


def click_button(button):
    """
    Click on a button. pass in damvision.Button enums.
    """
    x, y = button.value
    pyautogui.moveTo(scaling.scale_xy_offset(x, y))
    pyautogui.mouseDown()
    pyautogui.mouseUp()

    logger.debug(str(button) + " clicked")


def extract_hit_list():
    """
    Function to locate and extract text from the list of search results.
    @return number of hits (good for keeping track of pages) and the search results in a tuple array of (name, author) always with length 5.
    @NOTE that the OCRs used are still not good. It will have around 80% accuracy. Also, if number of hits cannot be determined, it will return -1.
    """

    results = []

    x, y = scaling.scale_xy_offset(1940, 360)
    l, w = scaling.scale_xy(115, 45)

    num_results_screenshot = pyautogui.screenshot(region=(x, y, l, w))
    # num_results_screenshot.save('num.png') # DEBUG PURPOSES ONLY
    num_results_screenshot = asarray(num_results_screenshot)
    num_results = pytesseract.image_to_string(num_results_screenshot, lang='eng').replace("\n", "")
    logger.debug("num_results = " + num_results)
    try:
        num_results = int(num_results.replace("\n", ""))
    except ValueError:
        logger.warning("OCR for hit number failed. Defaulting to -1.")
        num_results = -1
    

    for i in range(5):

        x, y = scaling.scale_xy_offset(1425, 475 + i * 135)
        l, w = scaling.scale_xy(705, 60)
        
        name_screenshot = pyautogui.screenshot(region=(x, y, l, w))
        # name_screenshot.save('name' + str(i) + '.png') # DEBUG PURPOSES ONLY
        name_screenshot = asarray(name_screenshot)
        
        name = pytesseract.image_to_string(name_screenshot, lang='jpn')
        if name == '':
            try:
                name = reader.readtext(name_screenshot, paragraph=True)[-1][-1]
            except IndexError:
                pass

        x, y = scaling.scale_xy_offset(1425, 545 + i * 135)
        l, w = scaling.scale_xy(705, 42)

        author_screenshot = pyautogui.screenshot(region=(x, y, l, w))
        # author_screenshot.save('author' + str(i) + '.png') # DEBUG PURPOSES ONLY
        author_screenshot = asarray(author_screenshot)

        author = pytesseract.image_to_string(author_screenshot, lang='jpn')
        if author == '':
            try:
                author = reader.readtext(author_screenshot, paragraph=True)[-1][-1]
            except IndexError:
                pass

        results.append((name.replace("\n", ""), author.replace("\n", "")))

    logger.debug("results list extracted with " + str(num_results) + " hits.\nresults = " + str(results))

    return num_results, results

def search_loading():

    # Take a full screenshot and convert it to grayscale
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

    # Read the image and convert it to grayscale
    template = cv2.imread('./images/korekana.png', cv2.IMREAD_GRAYSCALE)

    # Perform matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    logger.debug("これかな detected with confidence " + str(max_val))

    x, y = max_loc

    pyautogui.move(x, y)
    
    return True if max_val > 0.7 else False

def no_results():

    # Take a full screenshot and convert it to grayscale
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

    # Read the image and convert it to grayscale
    template = cv2.imread('./images/noresults.png', cv2.IMREAD_GRAYSCALE)

    # Perform matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    logger.debug("no results detected with confidence " + str(max_val))
    
    return True if max_val > 0.7 else False

def on_reserve_page():

    # Take a full screenshot and convert it to grayscale
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

    # Read the image and convert it to grayscale
    template = cv2.imread('./images/reserve.png', cv2.IMREAD_GRAYSCALE)

    # Perform matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    logger.debug("reserve button detected with confidence " + str(max_val))
    
    return True if max_val > 0.995 else False

def playing_song():

    x, y = scaling.scale_xy_offset(190, 1060)
    l, w = scaling.scale_xy(405, 45)

    name_screenshot = pyautogui.screenshot(region=(x, y, l, w))
    name_screenshot.save('song.png') # DEBUG PURPOSES ONLY
    num_results_screenshot = asarray(name_screenshot)

    name_screenshot = asarray(pyautogui.screenshot(imageFilename='fdsfsd.png', region=(x, y, l, w)))
    name = pytesseract.image_to_string(name_screenshot, lang='jpn')
    if name == '':
        try:
            name = reader.readtext(name_screenshot, paragraph=True)[-1][-1]
        except IndexError:
            name = None
            pass