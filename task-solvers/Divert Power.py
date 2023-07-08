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
if data["task_locations"][data["tasks"].index("Divert Power")] == "Electrical":
    x = dimensions[0] + round(dimensions[2] / 3.26)
    y = dimensions[1] + round(dimensions[3] / 1.415)

    x_offset = round(dimensions[2] / 19.7)

    if is_urgent_task():
        click_close()
        raise SystemExit(0)

    exit = False
    for i in range(0, 8):
        pixel = pyautogui.pixel(x= x + x_offset*i, y= y)
        if pixel[0] > 250 and pixel[1] > 96 and pixel[1] < 100 and pixel[2] < 2:
            pyautogui.moveTo(x + x_offset*i, y)
            pyautogui.dragTo(x + x_offset*i, y - round(dimensions[3] / 10.5), duration=0.2, tween=pyautogui.easeOutQuad)
            #break
    # 255 98 0
else:
    x = dimensions[0] + round(dimensions[2] / 2)
    y = dimensions[1] + round(dimensions[3] / 2)
    pyautogui.click(x,y)
