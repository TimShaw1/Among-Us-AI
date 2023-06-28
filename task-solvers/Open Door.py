from task_utility import *
import time
import pyautogui
from math import dist

click_use()
time.sleep(0.3)

PB_DOOR_LOCATIONS = [(37.641502, -10.066866), (38.974846, -12.105497), (25.77523, -24.922377), (23.96007, -23.106699)]
data = getGameData()

if data["map_id"].upper() == "PB":
    for loc in PB_DOOR_LOCATIONS:
        if dist(loc, data["position"]) < 1:
            raise SystemExit(0)

dimensions = get_dimensions()

x = dimensions[0] + round(dimensions[2] / 2.61)
y = dimensions[1] + round(dimensions[3] / 5.14)

x_offset = round(dimensions[2] / 5.77)
y_offset = round(dimensions[3] / 5.57)

for i in range(2):
    for j in range(4):
        pyautogui.click(x + x_offset*i, y + y_offset*j)