from task_utility import *
import time
import pyautogui

click_use()
time.sleep(0.3)

dimensions = get_dimensions()
dimensions[0] += dimensions[2] / 2.27
dimensions[1] += dimensions[3] / 3.88

y_offset = dimensions[3] / 2.16

pyautogui.moveTo(dimensions[0], dimensions[1])
pyautogui.dragTo(dimensions[0], dimensions[1] + y_offset, 0.4)
time.sleep(4)
pyautogui.click()
time.sleep(1)

if not is_task_done("Fill Canisters"):
    pyautogui.moveTo(dimensions[0], dimensions[1])
    pyautogui.dragTo(dimensions[0], dimensions[1] + y_offset, 0.4)
    time.sleep(4)
    pyautogui.click()