import numpy as np
import cv2
from task_utility import *
import time
import pyautogui

click_use()
time.sleep(0.8)

dimensions = get_dimensions()
resize_images(dimensions, "Stabilize Steering")

dimensions[0] += round(dimensions[2] / 3.69)
dimensions[1] += round(dimensions[3] / 10.38)
dimensions[2] = round(dimensions[2] / 2.21)
dimensions[3] = round(dimensions[3] / 1.25)
center = (round(dimensions[2] / 2), round(dimensions[3] / 2))

pos = pyautogui.locateCenterOnScreen(f"{get_dir()}\\task-solvers\\cv2-templates\\Stabilize Steering resized\\crosshair.png", confidence=0.75, region=dimensions)

pyautogui.moveTo(pos)
pyautogui.dragTo(center[0] + dimensions[0], center[1] + dimensions[1], duration=0.2, tween=pyautogui.easeOutQuad)