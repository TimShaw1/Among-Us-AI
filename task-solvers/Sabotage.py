import numpy as np
import cv2
from task_utility import *
import time
import pyautogui
import copy

dimensions = get_dimensions()

s_dimensions = copy.deepcopy(dimensions)
s_dimensions[0] = dimensions[0] + round(dimensions[2] / 1.42)
s_dimensions[1] = dimensions[1] + round(dimensions[3] / 1.207)
s_dimensions[2] = round(dimensions[2] / 14.88)
s_dimensions[3] = round(dimensions[3] / 10.38)

wake()

pyautogui.click(s_dimensions[0] + round(s_dimensions[2] / 2), s_dimensions[1] + round(s_dimensions[3] / 2))

x = dimensions[0] + round(dimensions[2] / 10.97)
y = dimensions[1] + round(dimensions[3] / 2.06)

pyautogui.click(x,y)
time.sleep(1/30)

x = dimensions[0] + round(dimensions[2] / 1.46)
y = dimensions[1] + round(dimensions[3] / 2.28)

pyautogui.click(x,y)
time.sleep(1/30)

x = dimensions[0] + round(dimensions[2] / 12.8)
y = dimensions[1] + round(dimensions[3] / 7.66)

pyautogui.click(x,y)


#220 37 0