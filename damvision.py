import cv2
import pyautogui
import numpy as np
from enum import Enum
from loguru import logger
import easyocr
import pytesseract
from numpy import asarray

reader = easyocr.Reader(['ja','en'])
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # you may have to install https://github.com/UB-Mannheim/tesseract/wiki

class Button(Enum):
    RESTART = './images/restart.png'
    # PAUSE = './images/pause.png' # gotta figure out how this button actually works in the app, appears greyed out all the time
    SKIP = './images/skip.png'
    KEYDOWN = './images/keydown.png'
    KEYUP = './images/keyup.png'
    BACK = './images/back.png'
    TOP = './images/top.png'

    SEARCH_KEYWORD = './images/search_keyword.png'
    SEARCH_SONGNAME = './images/search_songname.png'
    SEARCH_ARTISTNAME = './images/search_artistname.png'

    SEARCH = './images/search.png'

    RESERVE = './images/reserve.png'

    MOUSE_RESET = './images/logo.png'



# Function to recognize a button given an image as an input (see above) and click on it.
# @return confidence value. If the button exists, it should be >0.99.
def click_button(button):

    image_path = button.value

    # Take a full screenshot and convert it to grayscale
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

    # Read the button image and convert it to grayscale
    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Perform matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Get position of the button
    button_pos = max_loc

    if button_pos:
        x, y = button_pos
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        pyautogui.mouseDown()
        pyautogui.mouseUp()

    logger.debug("Button " + str(button) + " clicked with confidence " + str(max_val))
    
    return max_val



# Function to locate and extract text from the list of search results.
# @return number of hits (good for keeping track of pages) and the search results in a tuple array of (name, author) always with length 5.
# NOTE that the OCRs used are still not good. It will have around 80% accuracy. Also, if number of hits cannot be determined, it will return -1.
def extract_hit_list():

    results = []

    # Take a full screenshot and convert it to grayscale
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

    # Read the border image and convert it to grayscale
    border = cv2.imread('./images/results_border.png', cv2.IMREAD_GRAYSCALE)

    # Perform matching
    result = cv2.matchTemplate(screenshot, border, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    x, y = max_loc

    num_results_screenshot = asarray(pyautogui.screenshot(region=(x+620, y+70, 100, 40))) #TODO change this for 4 digit numbers
    num_results = pytesseract.image_to_string(num_results_screenshot, lang='eng').replace("\n", "")
    logger.debug("num_results = " + num_results)
    try:
        num_results = int(num_results.replace("\n", ""))
    except ValueError:
        logger.warning("OCR for hit number failed. Defaulting to -1.")
        num_results = -1

    for i in range(5):
        
        name_screenshot = asarray(pyautogui.screenshot(region=(x+90, y+180 + i * 135, 710, 60)))
        name = pytesseract.image_to_string(name_screenshot, lang='jpn')
        if name == '':
            try:
                name = reader.readtext(name_screenshot, paragraph=True)[-1][-1]
            except IndexError:
                pass

        author_screenshot = asarray(pyautogui.screenshot(region=(x+90, y+250 + i * 135, 710, 42)))
        author = pytesseract.image_to_string(author_screenshot, lang='jpn')
        if author == '':
            try:
                author = reader.readtext(author_screenshot, paragraph=True)[-1][-1]
            except IndexError:
                pass

        results.append((name.replace("\n", ""), author.replace("\n", "")))

    logger.info("results list extracted with " + str(num_results) + " hits.")

    logger.debug("results = " + str(results))

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
    
    return True if max_val > 0.995 else False

# def search_blank():

#     # Take a full screenshot and convert it to grayscale
#     screenshot = pyautogui.screenshot()
#     screenshot = np.array(screenshot)
#     screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

#     # Read the image and convert it to grayscale
#     template = cv2.imread('./images/search_blank.png', cv2.IMREAD_GRAYSCALE)

#     # Perform matching
#     result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

#     logger.debug("search results blank? detected with confidence " + str(max_val))
    
#     return True if max_val > 0.99 else False

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
    
    return True if max_val > 0.99 else False

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

    # Take a full screenshot and convert it to grayscale
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

    # Read the image and convert it to grayscale
    template = cv2.imread('./images/songplaying.png', cv2.IMREAD_GRAYSCALE)

    # Perform matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    logger.debug("playing song? detected with confidence " + str(max_val))

    x, y = max_loc

    name_screenshot = asarray(pyautogui.screenshot(region=(x+90, y, 550, 60)))
    name = pytesseract.image_to_string(name_screenshot, lang='jpn')
    if name == '':
        try:
            name = reader.readtext(name_screenshot, paragraph=True)[-1][-1]
        except IndexError:
            name = None
            pass
    
    return name if max_val > 0.99 else None