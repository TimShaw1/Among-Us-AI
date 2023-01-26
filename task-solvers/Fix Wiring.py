import numpy as np
import cv2
from task_utility import *
import time

dimensions = get_dimensions()
left_dimensions = dimensions

left_dimensions[0] += round(left_dimensions[2] / 3.8)
left_dimensions[2] /= 18
left_dimensions[2] = round(left_dimensions[2])
left_dimensions[1] += 200
left_dimensions[3] /= 1.5
left_dimensions[3] = round(left_dimensions[3])
print(left_dimensions)

right_dimensions = left_dimensions
right_dimensions[0] += 800
print(right_dimensions)

click_use()
time.sleep(0.8)

screenshot = get_screenshot(dimensions)

wire_colors = ["red", "blue", "yellow", "pink"]
wire_positions = []

for color in wire_colors:
    left = pyautogui.locateCenterOnScreen(f"{get_dir()}\\task-solvers\\cv2-templates\\Fix Wiring\\{color}Wire.png", confidence=0.6, region=left_dimensions)
    right = pyautogui.locateCenterOnScreen(f"{get_dir()}\\task-solvers\\cv2-templates\\Fix Wiring\\{color}Wire.png", confidence=0.6, region=right_dimensions)
    wire_positions.append((left, right))

for line in wire_positions:
    pyautogui.moveTo(line[0][0] + 100, line[0][1])
    time.sleep(2)
