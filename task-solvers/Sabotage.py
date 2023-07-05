import numpy as np
import cv2
from task_utility import *
import time
import pyautogui
import copy
import random

dimensions = get_dimensions()
data = getGameData()

s_dimensions = copy.deepcopy(dimensions)
s_dimensions[0] = dimensions[0] + round(dimensions[2] / 1.42)
s_dimensions[1] = dimensions[1] + round(dimensions[3] / 1.207)
s_dimensions[2] = round(dimensions[2] / 14.88)
s_dimensions[3] = round(dimensions[3] / 10.38)

wake()

pyautogui.click(s_dimensions[0] + round(s_dimensions[2] / 2), s_dimensions[1] + round(s_dimensions[3] / 2))

rand = random.randint(1,3)
rand = 3

reactor_dict = {
    "SHIP": (dimensions[0] + round(dimensions[2] / 10.97), dimensions[1] + round(dimensions[3] / 2.06)), 
    "PB" : (dimensions[0] + round(dimensions[2] / 1.48), dimensions[1] + round(dimensions[3] / 2.49))
}

o2_dict = {
    "SHIP": (dimensions[0] + round(dimensions[2] / 1.46), dimensions[1] + round(dimensions[3] / 2.28)), 
    "PB": (dimensions[0] + round(dimensions[2] / 4.17), dimensions[1] + round(dimensions[3] / 2.2)) # lights since no o2
}

lights_dict = {
    "SHIP": (dimensions[0] + round(dimensions[2] / 2.46), dimensions[1] + round(dimensions[3] / 1.54)), 
    "PB": (dimensions[0] + round(dimensions[2] / 4.17), dimensions[1] + round(dimensions[3] / 2.2))
}

# TODO: hardcoded to skeld
# reactor
if rand == 1:
    x, y = reactor_dict[data["map_id"].upper()]

    pyautogui.click(x,y)
    time.sleep(1/30)

# oxygen
elif rand == 2: 
    x, y = o2_dict[data["map_id"].upper()]

    pyautogui.click(x,y)
    time.sleep(1/30)

# lights
else:
    x, y = lights_dict[data["map_id"].upper()]

    pyautogui.click(x,y)
    time.sleep(1/30)

close_dict = {
    "SHIP": (dimensions[0] + round(dimensions[2] / 12.8), dimensions[1] + round(dimensions[3] / 7.66)), 
    "PB" : (dimensions[0] + round(dimensions[2] / 6.06), dimensions[1] + round(dimensions[3] / 8.06))
}

x, y = close_dict[data["map_id"].upper()]

pyautogui.click(x,y)


#220 37 0