from task_utility import *
import copy
import pyautogui
import time

def get_report_button_pos() -> tuple:
    dimensions = get_dimensions()

    x = dimensions[0] + round(dimensions[2] / 1.19)
    y = dimensions[1] + round(dimensions[3] / 1.17)
    return (x,y)

def can_report() -> bool:
    x,y = get_report_button_pos()
    col = pyautogui.pixel(x, y)
    return col[0] > 200 and col[2] < 5

# DEPRECIATED
def report() -> None:
    if not can_report():
        return
    wake()
    pyautogui.click(get_report_button_pos())