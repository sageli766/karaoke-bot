import pyautogui
from loguru import logger
from PIL import Image
import os

window_size = (2258, 1307) # Size of the DAM window on a 2560x1440 screen

def get_window_pos():
    """
    Get the left and top position of the DAM window (x, y).
    """
    window = pyautogui.getWindowsWithTitle("(KARAOKE@DAM)")[0]
    return window.left, window.top

def get_window_size():
    """
    Get the width and height of the DAM window.
    """
    window = pyautogui.getWindowsWithTitle("(KARAOKE@DAM)")[0]
    return window.width, window.height

def get_scaling_factors():
    """
    Calculate scaling ratios based on the detected DAM window size from the original (2560, 1440)
    """
    window_width, window_height = get_window_size()

    scaling_ratio_x = window_width / window_size[0]
    scaling_ratio_y = window_height / window_size[1]

    return scaling_ratio_x, scaling_ratio_y

def scale_xy(x, y):
    """
    Returns a tuple of int(x, y) with scaled x and y.
    """
    x_scale, y_scale = get_scaling_factors()
    return int(x * x_scale), int(y * y_scale)

def scale_xy_offset(offset_x, offset_y):
    """
    Returns a tuple of int(x, y) with scaled x and y offsets from the window's top left position.
    """
    x_scale, y_scale = get_scaling_factors()
    x, y = get_window_pos()
    return int(x + (offset_x * x_scale)), int(y + (offset_y * y_scale))

def check_images():
    monitor_size = (1920, 1080)
    current_size = pyautogui.size()
    current_window_size = get_window_size()
    reference_dir = "./images/reference"
    image_dir = "./images"

    if (window_size != current_window_size or monitor_size != current_size) and all(not os.path.isfile(os.path.join(image_dir, filename)) for filename in os.listdir(image_dir)):

        prop = (current_size[0] / monitor_size[0], current_size[1] / monitor_size[1])

        logger.debug("Current DAM window size " + str(current_window_size) + " != reference size " + str(window_size) + " and rescaled images not detected. Creating rescaled images.")

        x_scale, y_scale = get_scaling_factors()

        # Iterate through each image ending with "_og.png" in ./images directory
        for filename in os.listdir(reference_dir):
            if filename.endswith("_og.png"):
                img_path = os.path.join(reference_dir, filename)
                img = Image.open(img_path)
                resized_img = img.resize((int(img.size[0] * x_scale * prop[0]), int(img.size[1] * y_scale * prop[1])))

                # Save the resized image without "_og" in its name
                new_filename = filename.replace("_og.png", ".png")
                resized_img.save(os.path.join(image_dir, new_filename))

logger.debug(str(pyautogui.getWindowsWithTitle("(KARAOKE@DAM)")[0]))
check_images()
