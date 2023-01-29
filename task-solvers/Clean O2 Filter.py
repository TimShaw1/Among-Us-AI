from task_utility import *
import time
import cv2
import copy

click_use()
time.sleep(0.8)

dimensions = get_dimensions()
s_dimensions = copy.deepcopy(dimensions)

s_dimensions[0] += round(dimensions[2] / 2.73)
s_dimensions[1] += round(dimensions[3] / 10.49)

s_dimensions[2] /= 2.75
s_dimensions[2] = round(s_dimensions[2])
s_dimensions[3] /= 1.24
s_dimensions[3] = round(s_dimensions[3])

vent_pos = (dimensions[0] + round(dimensions[2] / 3.11), dimensions[1] + round(dimensions[3] / 2))

screenshot = get_screenshot(s_dimensions)
print(s_dimensions)

while not is_task_done("Clean O2 Filter"):
    screenshot = get_screenshot(s_dimensions)
    for x in range(0, screenshot.width, 2):
        for y in range(0, screenshot.height, 2):
            pixel = screenshot.getpixel((x, y))

            if pixel[0] > 130 and pixel[0] < 205 and pixel[2] < 70 and pixel[2] > 20:
                pyautogui.moveTo(x + s_dimensions[0] + 10, y + s_dimensions[1] + 10)
                pyautogui.dragTo(vent_pos[0], vent_pos[1], duration=0.2, tween=pyautogui.easeOutQuad)
                screenshot = get_screenshot(s_dimensions)
                break
        if (is_task_done("Clean O2 Filter")):
            break

# Color is 200 149 66
#       or 137  40 24