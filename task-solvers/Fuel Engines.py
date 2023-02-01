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

x = dimensions[0] + round(dimensions[2] / 1.31)
y = dimensions[1] + round(dimensions[3] / 1.24)

pyautogui.moveTo((x,y))
pyautogui.dragTo(x,y, duration=2.8)