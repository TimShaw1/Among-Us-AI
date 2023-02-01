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
pyautogui.click(dimensions[0] + round(dimensions[2] / 2), dimensions[1] + round(dimensions[3] / 2))

dimensions[0] += round(dimensions[2] / 3.52)
dimensions[1] += round(dimensions[3] / 6.24)
dimensions[2] = round(dimensions[2] / 2.31)
dimensions[3] = round(dimensions[3] / 1.49)

screenshot = get_screenshot(dimensions)
offset = 100

while not is_task_done("Vent Cleaning"):
    for x in range(0, screenshot.width, offset):
        if is_task_done("Vent Cleaning"):
            break
        for y in range(0, screenshot.height, offset):
            pyautogui.click(dimensions[0] + x, dimensions[1] + y)
            if is_task_done("Vent Cleaning"):
                break

    offset = round(offset / 2)