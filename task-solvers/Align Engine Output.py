import numpy as np
import cv2
from task_utility import *
import time
import pyautogui

click_use()
time.sleep(0.8)

dimensions = get_dimensions()

dimensions[0] += round(dimensions[2] / 1.68)
dimensions[2] /= 7.4
dimensions[2] = round(dimensions[2])
y_center = ((dimensions[1] + round(dimensions[1] / 1.2) + dimensions[3]) / 2)

# Color is 88 88 95

while not is_task_done("Align Engine Output"):
    screenshot = get_screenshot(dimensions)
    exit = False

    if is_urgent_task():
        click_close()
        raise SystemExit(0)

    for x in range(screenshot.width):
        for y in range(screenshot.height):
            pixel = screenshot.getpixel((x, y))
            if pixel[1] < 90 and pixel[1] > 86 and pixel[0] < 90 and pixel[0] > 86 and pixel[2] < 100 and pixel[2] > 90:
                pyautogui.moveTo(dimensions[0] + x + 10, dimensions[1] + y) 
                pyautogui.dragTo(dimensions[0] + x + 10, y_center, abs((dimensions[1] + y) - y_center) / 400)
                raise SystemExit(0)
