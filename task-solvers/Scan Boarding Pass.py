from task_utility import *
import time
import pyautogui

click_use()
time.sleep(0.3)

dimensions = get_dimensions()

x = dimensions[0] + round(dimensions[2] / 3.39)
y = dimensions[1] + round(dimensions[3] / 2.08)

pyautogui.click(x,y)
time.sleep(0.4)

x = dimensions[0] + round(dimensions[2] / 2.73)
y = dimensions[1] + round(dimensions[3] / 9.23)

pyautogui.click(x,y)
time.sleep(0.4)

x = dimensions[0] + round(dimensions[2] / 2.73)
x2 = dimensions[0] + round(dimensions[2] / 1.46)
y = dimensions[1] + round(dimensions[3] / 2)

pyautogui.moveTo(x,y)
pyautogui.dragTo(x2, y, 0.5)
while not is_task_done("Scan Boarding Pass"):
    time.sleep(1/15)