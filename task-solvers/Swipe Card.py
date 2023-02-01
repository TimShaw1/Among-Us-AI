import numpy as np
import cv2
from task_utility import *
import time
import cv2
import copy

click_use()
time.sleep(0.8)

dimensions = get_dimensions()

x = dimensions[0] + round(dimensions[2] / 2.5)
y = dimensions[1] + round(dimensions[3] / 1.32)

pyautogui.click(x,y)
time.sleep(0.8)

x = dimensions[0] + round(dimensions[2] / 3.33)
y = dimensions[1] + round(dimensions[3] / 2.51)

pyautogui.moveTo(x,y)

x = dimensions[0] + round(dimensions[2] / 1.3)
# y is the same

def easeInOutExpo(x):
    if x == 0 or x == 1:
        return x
    else:
        if x < 0.5:
            return pow(2, 20 * x - 10) / 2
        else:
            return 2 - pow(2, -20 * x + 10) / 2

pyautogui.dragTo(x,y, duration=3.1)