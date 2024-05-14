import cv2
import pyautogui
import numpy as np
from loguru import logger
# import easyocr
# import pytesseract
# from numpy import asarray

# reader = easyocr.Reader(['ja','en'])
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # you may have to install https://github.com/UB-Mannheim/tesseract/wiki

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
    
    return True if max_val > 0.7 else False

# def playing_song():

#     x, y = scaling.scale_xy_offset(200, 1065)
#     l, w = scaling.scale_xy(570, 50)

#     name_screenshot = pyautogui.screenshot(region=(x, y, l, w))
#     # name_screenshot.save('song.png') # DEBUG PURPOSES ONLY
#     name_screenshot = asarray(name_screenshot)

#     name = pytesseract.image_to_string(name_screenshot, lang='jpn')
#     name = name.replace("\n", "")
#     if 'ボタンを押して' in name or '楽曲を予約して' in name or '楽曲再生準備' in name:
#         return None
#     if name == '':
#         try:
#             name = reader.readtext(name_screenshot, paragraph=True)[-1][-1]
#         except IndexError:
#             name = None
#             pass
    
#     logger.debug(name)

#     return name