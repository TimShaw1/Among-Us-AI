import time
from task_utility import *
import pyautogui

click_use()
time.sleep(0.8)

dimensions = get_dimensions()

pyautogui.moveTo(dimensions[0] + round(dimensions[2] / 1.96), dimensions[1] + round(dimensions[3] / 1.56))

pyautogui.mouseDown()
while not is_task_done("Reset Reactor"):
    time.sleep(1/30)

pyautogui.mouseUp()