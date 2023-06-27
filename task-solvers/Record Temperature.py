from task_utility import *
import time
import pyautogui
import copy
import pytesseract
import re

click_use()
time.sleep(0.3)

dimensions = get_dimensions()

s_dimensions = copy.deepcopy(dimensions)
s_dimensions[0] = round(s_dimensions[0] + s_dimensions[2] / 4.3)
s_dimensions[1] = round(s_dimensions[1] + s_dimensions[2] / 2.66)
s_dimensions[2] = round(s_dimensions[2] / 5.13)
s_dimensions[3] = round(s_dimensions[3] / 6.88)

x = dimensions[0] + round(dimensions[2] / 3.03)
y_hi = dimensions[1] + round(dimensions[3] / 3.2)
y_low = dimensions[1] + round(dimensions[3] / 1.7)

screenshot = get_screenshot([x, y_hi, s_dimensions[2], s_dimensions[3]])
screenshot.show()
text = pytesseract.image_to_string(screenshot.convert("L"))
nums = re.findall(r'\b\d+\b', text)[0]
print(nums)