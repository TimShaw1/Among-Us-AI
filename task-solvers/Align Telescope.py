import time
from task_utility import *
import pyautogui
from math import sin,cos
import numpy

click_use()
time.sleep(0.8)

dim = get_dimensions()

angles = {"broken" : 1.29, "nebula" : 1.94, "dyson" : 0.9, "ship" : 3.25, "galaxy" : 3.91, "green" : 4.84, "gas" : 5.69}
times = {"broken" : 0.9, "nebula" : 2, "dyson" : 2.5, "ship" : 1.4, "galaxy" : 2, "green" : 2, "gas" : 2}

x = dim[0] + round(dim[2] / 1.35)
y = dim[1] + round(dim[3] / 1.24)
pixel = pyautogui.pixel(x,y)
if is_urgent_task():
    raise SystemExit(0)

name = ""
if max(abs(numpy.subtract(pixel, (192, 190, 188)))) < 3:
    name = "dyson"

elif max(abs(numpy.subtract(pixel, (68, 73, 71)))) < 3:
    name = "ship"

elif max(abs(numpy.subtract(pixel, (78, 74, 107)))) < 3:
    name = "gas"

elif max(abs(numpy.subtract(pixel, (255, 255, 255)))) < 3:
    name = "galaxy"

elif max(abs(numpy.subtract(pixel, (84, 114, 118)))) < 3 or max(abs(numpy.subtract(pixel, (76, 102, 107)))) < 3:
    name = "nebula"

elif max(abs(numpy.subtract(pixel, (10, 6, 8)))) < 3:
    name = "broken"

elif max(abs(numpy.subtract(pixel, (93, 133, 124)))) < 3 or max(abs(numpy.subtract(pixel, (77, 108, 102)))) < 3:
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
