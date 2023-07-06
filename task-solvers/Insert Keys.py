from task_utility import *
import time
import pyautogui

click_use()
time.sleep(0.3)

dimensions = get_dimensions()

#get_screen_ratio(dimensions) #2.08 10.5

x = round(dimensions[0] + dimensions[2] / 2.08)
y = round(dimensions[1] + dimensions[3] / 17.14)

y2 = round(dimensions[1] + dimensions[3] / 10.5)

x_offset = round(dimensions[2] / 6.64)
y_offset = round(dimensions[3] / 5.87)

if is_urgent_task():
    raise SystemExit(0)

# red > 200
for i in range(3):
    for j in range(5):
        for q in range(4):
            pixel = pyautogui.pixel(x + i*x_offset, y2 + y_offset*j + q)
            if pixel[0] > 200:
                pyautogui.moveTo(dimensions[0] + round(dimensions[2] / 4.25), dimensions[1] + round(dimensions[3] / 1.49))
                pyautogui.moveTo(x + i*x_offset, y2 + j*y_offset + 20, 0.7)
                pyautogui.moveTo(x + i*x_offset + round(dimensions[2] / 9.6), y2 + j*y_offset + round(dimensions[3] / 11), 0.3)
                raise SystemExit(0)

# 206 130 24

