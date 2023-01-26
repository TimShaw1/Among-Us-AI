import numpy as np
import cv2
from task_utility import *
import time
import cv2

click_use()
time.sleep(0.8)

dimensions = get_dimensions()
dimensions[0] += round(dimensions[2] / 3.44)
dimensions[2] /= 4
dimensions[2] = round(dimensions[2])
dimensions[1] += round(dimensions[3] / 7.82)
dimensions[3] /= 1.54
dimensions[3] = round(dimensions[3])

color = (30,80,40)
max_diff = 6
task = "Clear Asteroids"

while not is_task_done(task):
    screenshot = get_screenshot(dimensions)
    exit = False

    for x in range(screenshot.width):
        if not exit:
            for y in range(screenshot.height):
                pixel = screenshot.getpixel((x, y))
                if pixel[1] < 70 and pixel[1] > 50 and pixel[0] < 30 and pixel[0] > 10 and pixel[2] < 70:
                    pyautogui.click(dimensions[0] + x, dimensions[1] + y) 
                    exit = True
                    break
        else:
            break
    exit = False