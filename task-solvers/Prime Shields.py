import numpy as np
import cv2
from task_utility import *
import time
import cv2
import copy
import pyautogui

click_use()
time.sleep(0.8)

dimensions = get_dimensions()

s_dimensions = copy.deepcopy(dimensions)
s_dimensions[0] += round(dimensions[2] / 2.62)
s_dimensions[1] += round(dimensions[3] / 3.61)
s_dimensions[2] = round(dimensions[2] / 4.29)
s_dimensions[3] = round(dimensions[3] / 2.24)

screenshot = get_screenshot(s_dimensions)

exit = False
for x in range(0, screenshot.height - 10, 5):
    if exit:
        break
    for y in range(0, screenshot.width - 10, 5):
        pixel = screenshot.getpixel((x,y))

        if (pixel[0] - 242) < 2 and (pixel[1] - 24) < 2 and (pixel[2] - 28) < 2:
            pyautogui.click(s_dimensions[0] + x + 20, s_dimensions[1] + y + 20)
            screenshot = get_screenshot(s_dimensions)
            if is_task_done("Prime Shields"):
                exit = True
                break

# 242,24,28