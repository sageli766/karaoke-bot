import damcontrol
import time
from PIL import Image
import pyautogui
import scaling

# img = Image.open('./images/results_border.png')
# resized_img = img.resize(scaling.rescale(img.size[0], img.size[1]))
# resized_img.save('./images/results_border1.png')

# time.sleep(1)
# window = pyautogui.getWindowsWithTitle("(KARAOKE@DAM)")[0]
# window.activate()


scaling.check_images()

# damcontrol.extract_hit_list()