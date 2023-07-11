import time
from task_utility import *
import pyautogui
import copy

click_use()
time.sleep(0.8)

dimensions = get_dimensions()

x = dimensions[0] + round(dimensions[2] / 3.12)
y = dimensions[1] + round(dimensions[3] / 1.2)
offset = round(dimensions[2] / 11.03)

if is_urgent_task():
    click_close()
    raise SystemExit(0)
screenshot = get_screenshot(dimensions)
if is_urgent_task():
    click_close()
    raise SystemExit(0)

for i in range(5):
    color = screenshot.getpixel((x + i * offset - dimensions[0], y - dimensions[1]))
    if color[1] < 100:
        pyautogui.click(x + i * offset, y - round(dimensions[3] / 7.5))
        time.sleep(0.2)