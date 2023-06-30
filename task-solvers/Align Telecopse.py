import time
from task_utility import *
import pyautogui
import vgamepad as vg
from math import sin,cos
import random

click_use()
time.sleep(0.8)

dim = get_dimensions()

angles = {"broken" : 1.29, "nebula" : 1.94, "dyson" : 0.9, "ship" : 3.25, "galaxy" : 3.91, "green" : 4.84, "gas" : 5.69}
times = {"broken" : 0.9, "nebula" : 2, "dyson" : 2.5, "ship" : 1.4, "galaxy" : 2, "green" : 2, "gas" : 2}

gamepad = vg.VX360Gamepad()

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

def angle_to_gamepad(angle):
    x = round(cos(angle) + random.randint(0,5) / 1000, 5)
    y = round(sin(angle) + random.randint(0,5) / 1000, 5)

    x = 1 if x > 1 else x
    y = 1 if y > 1 else y
    return (x, y)

wake()
g_points = angle_to_gamepad(angles[name])
gamepad.left_joystick_float(x_value_float=g_points[0], y_value_float=g_points[1])
gamepad.update()
time.sleep(times[name])
gamepad.reset()
