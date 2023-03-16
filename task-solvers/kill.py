from task_utility import *
import copy
import pyautogui
import time

def get_kill_button_pos() -> tuple:
    dimensions = get_dimensions()

    x = dimensions[0] + round(dimensions[2] / 1.08)
    y = dimensions[1] + round(dimensions[3] / 1.49)
    return (x,y)

def can_kill() -> bool:
    x,y = get_kill_button_pos()
    col = pyautogui.pixel(x, y)
    return col[0] > 200 and col[1] > 200 and col[2] > 200

def kill() -> None:
    if not can_kill():
        return
    wake()
    pyautogui.click(get_kill_button_pos())