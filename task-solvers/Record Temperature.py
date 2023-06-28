from task_utility import *
import time
import pyautogui
import copy
import pytesseract
import re
import cv2
import PIL
import numpy
from PIL import ImageFilter

click_use()
time.sleep(0.3)

dimensions = get_dimensions()

s_dimensions = copy.deepcopy(dimensions)
s_dimensions[0] = round(s_dimensions[0] + s_dimensions[2] / 4.3)
s_dimensions[1] = round(s_dimensions[1] + s_dimensions[3] / 2.66)
s_dimensions[2] = round(s_dimensions[2] / 5.5)
s_dimensions[3] = round(s_dimensions[3] / 6.9)

x = dimensions[0] + round(dimensions[2] / 3.03)
y_hi = dimensions[1] + round(dimensions[3] / 3.2)
y_low = dimensions[1] + round(dimensions[3] / 1.7)

data = getGameData()
if data["map_id"].upper() == "PB":
    if data["position"][1] > -8:
        while not is_task_done("Record Temperature"):
            pyautogui.click(x, y_low)
            #time.sleep(1/30)
    else:
        while not is_task_done("Record Temperature"):
            pyautogui.click(x, y_hi)
            #time.sleep(1/30)

"""
screenshot = get_screenshot(s_dimensions)
s2 = PIL.ImageOps.invert(screenshot.convert("L")).point(lambda p: 255 if p > 100 else 0).filter(ImageFilter.GaussianBlur(radius = 2))
text = pytesseract.image_to_string(s2, config="digits")
print(text)
nums = re.findall(r'\b\d+\b', text)[0]
print(nums)
"""