from task_utility import *
import pyautogui
import time

dimensions = get_dimensions()

wake()

pyautogui.click(dimensions[0] + round(dimensions[2] / 6.74), dimensions[1] + round(dimensions[3] / 1.15))
time.sleep(0.3)
pyautogui.click(dimensions[0] + round(dimensions[2] / 3.87), dimensions[1] + round(dimensions[3] / 1.17))