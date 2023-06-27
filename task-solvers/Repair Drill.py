from task_utility import *
import time
import pyautogui

click_use()
time.sleep(0.3)

dimensions = get_dimensions()
dimensions[0] += dimensions[2] / 2.45
dimensions[1] += dimensions[3] / 4.5

x_offset = dimensions[2] / 5.55
y_offset = dimensions[3] / 1.85

pyautogui.moveTo(dimensions[0], dimensions[1], duration=0.2)
for i in range(4):
    pyautogui.click()

pyautogui.moveTo(dimensions[0] + x_offset, dimensions[1], duration=0)
for i in range(4):
    pyautogui.click()

pyautogui.moveTo(dimensions[0] + x_offset, dimensions[1] + y_offset, duration=0)
for i in range(4):
    pyautogui.click()

pyautogui.moveTo(dimensions[0], dimensions[1] + y_offset, duration=0)
for i in range(4):
    pyautogui.click()