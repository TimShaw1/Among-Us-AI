import time
from task_utility import *
import pyautogui
import vgamepad as vg
from math import sin,cos
import random
import os
import sys

click_use()
time.sleep(0.8)

dim = get_dimensions()

angles = {"broken" : 1.29, "nebula" : 1.94, "dyson" : 0.9, "ship" : 3.25, "galaxy" : 3.91, "green" : 4.84, "gas" : 5.69}
times = {"broken" : 0.9, "nebula" : 2, "dyson" : 2.5, "ship" : 1.4, "galaxy" : 2, "green" : 2, "gas" : 2}

x = dim[0] + round(dim[2] / 1.35)
y = dim[1] + round(dim[3] / 1.24)
pixel = pyautogui.pixel(x,y)

name = ""
if pixel == (192, 190, 188):
    name = "dyson"

elif pixel == (68, 73, 71):
    name = "ship"

elif pixel == (78, 74, 107):
    name = "gas"

elif pixel == (255, 255, 255):
    name = "galaxy"

elif pixel == (84, 114, 118):
    name = "nebula"

elif pixel == (10, 6, 8):
    name = "broken"

elif pixel == (93, 133, 124):
    name = "green"

x_angle = cos(angles[name])
y_angle = -sin(angles[name])

x = dim[0] + round(dim[2] / 2)
y = dim[1] + round(dim[3] / 2)

move_amount = round(dim[2] / 3.84)
while not is_task_done("Align Telescope"):
    pyautogui.moveTo(x + move_amount*x_angle, y + move_amount*y_angle)
    pyautogui.mouseDown()
    pyautogui.moveTo(x, y, 0.6)
    pyautogui.mouseUp()
    time.sleep(1/15)
