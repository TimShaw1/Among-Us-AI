import time
from task_utility import *
import pyautogui

click_use()
time.sleep(0.3)

dim = get_dimensions()

x = dim[0] + round(dim[2] / 2.5)
y = dim[1] + round(dim[3] / 3.16)

x_offset = round(dim[2] / 10.6)
y_offset = round(dim[3] / 6)

# kinda bad but works
pyautogui.moveTo(x + x_offset, y)
for j in range(5):
    pyautogui.dragTo(x, y + y_offset, 0.2)
    pyautogui.dragTo(x + x_offset, y + 2*y_offset, 0.2)
    pyautogui.dragTo(x + 2*x_offset, y + y_offset, 0.2)
    pyautogui.dragTo(x + x_offset, y, 0.2)