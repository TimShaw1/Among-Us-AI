import numpy as np
import cv2
from task_utility import *
import os
import time

click_use()
time.sleep(0.8)

dimensions = get_dimensions()

dimensions[0] += round(dimensions[2] / 1.68)
dimensions[2] /= 7.68
dimensions[2] = round(dimensions[2])
y_center = ((dimensions[1] + round(dimensions[1] / 1.2) + dimensions[3]) / 2)

screenshot = get_screenshot(dimensions)

arrow_pos = None
arrow_names = ["Arrow", "arrowDown", "arrowUp"]

for name in arrow_names:
    arrow_pos = pyautogui.locateCenterOnScreen(f"C:\\projects\\AmongUs\\Among-Us-AI\\task-solvers\\cv2-templates\\Align Engine Output\\{name}.png", confidence=0.35, region=dimensions)
    if arrow_pos:
        break

pyautogui.moveTo(arrow_pos)
pyautogui.dragTo(arrow_pos[0], y_center, duration=0.3, tween=pyautogui.easeOutQuad)
