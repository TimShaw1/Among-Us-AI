import numpy as np
import cv2
from task_utility import *
import time
import pyautogui
import json

click_use()
time.sleep(0.8)

dimensions = get_dimensions()

x_start = dimensions[0] + round(dimensions[2] / 3.7)
y_start = dimensions[1] + round(dimensions[3] / 2.3)

x_offset = round(dimensions[2] / 16)
y_offset = round(dimensions[3] / 9)

button_x_offset = round(dimensions[2] / 3.11)

click_list = []
seen_pos = []

exit = False
while not is_task_done("Start Reactor"):
    screenshot = get_screenshot(dimensions)
    for i in range(3):
        if exit:
            break
        for j in range(3):
            pos = (x_start + x_offset * i, y_start + y_offset * j)
            pixel = pyautogui.pixel(pos[0], pos[1])
            if (abs(pixel[0] - 68)) < 2 and (abs(pixel[1] - 168)) < 2 and (abs(pixel[2] - 255)) < 2:
                if pos in seen_pos:
                    seen_pos.remove(pos)
                    exit = True
                    time.sleep(1/5)
                    break
                else:
                    time.sleep(1)
                    click_list.append(pos)

                    # Save history
                    with open('task-solvers\\reactor_list\\reactor_list.json', 'w') as f:
                        json.dump(click_list, f)
                    for cpos in click_list:
                        pyautogui.click(cpos[0] + button_x_offset, cpos[1])
                        seen_pos.append(cpos)
                        time.sleep(1/60)
                    exit = True
                    break
    exit = False

# Clear simon says history
with open('task-solvers\\reactor_list\\reactor_list.json', 'w') as f:
    json.dump([], f)

# 1 2 3
# 4 5 6
# 7 8 9

# 68,168,255