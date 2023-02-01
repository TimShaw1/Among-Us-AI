import numpy as np
import cv2
from task_utility import *
import time
import pyautogui

click_use()
time.sleep(0.8)

dimensions = get_dimensions()
dimensions[0] += round(dimensions[2] / 3.4)
dimensions[1] += round(dimensions[3] / 2.9)
dimensions[2] = round(dimensions[2] / 2.4)
dimensions[3] = round(dimensions[3] / 3.1)

for i in range(1, 11):
    pos = pyautogui.locateCenterOnScreen(f"{get_dir()}\\task-solvers\\cv2-templates\\Unlock Manifolds\\{i}.png", confidence=0.8, region=dimensions, grayscale=True)
    pyautogui.click(pos)
