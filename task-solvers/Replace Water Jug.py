from task_utility import *
import time
import pyautogui

click_use()
time.sleep(0.3)

dimensions = get_dimensions()

x = dimensions[0] + round(dimensions[2] / 2.02)
y = dimensions[1] + round(dimensions[3] / 6.75)

pyautogui.moveTo(x,y)
pyautogui.mouseDown()
time.sleep(7)
pyautogui.mouseUp()