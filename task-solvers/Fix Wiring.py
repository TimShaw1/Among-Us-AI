import numpy as np
import cv2
from task_utility import *
import time
import copy

dimensions = get_dimensions()
left_dimensions = copy.deepcopy(dimensions)

left_dimensions[0] += round(left_dimensions[2] / 3.8)
left_dimensions[2] /= 18
left_dimensions[2] = round(left_dimensions[2])
left_dimensions[1] += 200
left_dimensions[3] /= 1.5
left_dimensions[3] = round(left_dimensions[3])

right_dimensions = copy.deepcopy(left_dimensions)
right_dimensions[0] += 800

click_use()
time.sleep(0.8)

screenshot = get_screenshot(dimensions)

wire_colors = ["red", "blue", "yellow", "pink"]
wire_positions = []

for color in wire_colors:
    confidence = 0.7
    if color == "yellow":
        confidence = 0.6
    left = pyautogui.locateCenterOnScreen(f"{get_dir()}\\task-solvers\\cv2-templates\\Fix Wiring\\{color}Wire.png", confidence=confidence, region=left_dimensions)
    right = pyautogui.locateCenterOnScreen(f"{get_dir()}\\task-solvers\\cv2-templates\\Fix Wiring\\{color}Wire.png", confidence=confidence, region=right_dimensions)
    wire_positions.append([left, right])

for line in wire_positions:
    pyautogui.moveTo(line[0][0] + round(dimensions[2] / 32), line[0][1])
    pyautogui.dragTo(line[1][0] - round(dimensions[2] / 19.2), line[1][1], duration=0.2, tween=pyautogui.easeOutQuad)
