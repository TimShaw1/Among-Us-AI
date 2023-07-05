from task_utility import *
import time
import pyautogui

click_use()
time.sleep(0.3)

dimensions = get_dimensions()

x = round(dimensions[0] + dimensions[2] / 2.08)
y = round(dimensions[1] + dimensions[3] / 17.14)

x_offset = round(dimensions[2] / 6.64)

if is_urgent_task():
    raise SystemExit(0)

for i in range(3):
    for j in range(round(dimensions[3] / 1.2)):
        pixel = pyautogui.pixel(x + i*x_offset, y + j)
        if pixel[0] < 210 and pixel[0] > 204 and pixel[1] < 135 and pixel[1] > 125 and pixel[2] < 27:
            pyautogui.moveTo(dimensions[0] + round(dimensions[2] / 4.25), dimensions[1] + round(dimensions[3] / 1.49))
            pyautogui.dragTo(x + i*x_offset, y + j + 20, 0.7)
            pyautogui.dragTo(x + i*x_offset + round(dimensions[2] / 9.6), y + j + round(dimensions[3] / 11), 0.3)
            raise SystemExit(0)

# 206 130 24

