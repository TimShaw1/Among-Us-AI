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

data = getGameData()
while not data["task_locations"]:
    data = getGameData()
if data["task_locations"][data["tasks"].index("Divert Power")] == "Electrical":
    s_dimensions = copy.deepcopy(dimensions)
    s_dimensions[0] += round(dimensions[2] / 3.4)
    s_dimensions[1] += round(dimensions[3] / 1.62)
    s_dimensions[2] = round(dimensions[2] / 2.44)
    s_dimensions[3] = round(dimensions[3] / 4.34)

    screenshot = get_screenshot()
    if is_urgent_task():
        click_close()
        raise SystemExit(0)

    exit = False
    for x in range(0, screenshot.width, 10):
        if exit:
            break
        for y in range(0, screenshot.height, 2):
            pixel = screenshot.getpixel((x,y))
            if pixel[0] > 250 and pixel[1] > 96 and pixel[1] < 100 and pixel[2] < 2:
                pyautogui.moveTo(x + dimensions[0], y + dimensions[1])
                pyautogui.dragTo(x + dimensions[0], y + dimensions[1] - round(dimensions[3] / 10.5), duration=0.2, tween=pyautogui.easeOutQuad)
                exit = True
                break
    # 255 98 0
else:
    x = dimensions[0] + round(dimensions[2] / 2)
    y = dimensions[1] + round(dimensions[3] / 2)
    pyautogui.click(x,y)
