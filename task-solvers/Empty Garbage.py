import numpy as np
import cv2
from task_utility import *
import time
import cv2
import copy

click_use()
time.sleep(0.8)

dimensions = get_dimensions()

x = dimensions[0] + round(dimensions[2] / 1.5)
y = dimensions[1] + round(dimensions[3] / 2.52)
dest = (x, y + round(dimensions[3] / 3.85))

def easeOutNine(x):
    return 1 - pow(1 - x, 9)

pyautogui.moveTo((x,y))
pyautogui.dragTo(dest[0], dest[1], duration=2, tween=easeOutNine)