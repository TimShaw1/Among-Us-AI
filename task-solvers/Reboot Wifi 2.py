import time
from task_utility import *
import pyautogui

click_use()
time.sleep(0.8)

dim = get_dimensions()

with open("sendDataDir.txt") as f:
    line = f.readline().rstrip()
    WIFI_DATA_PATH = line + "\\wifiTaskData.txt"

def get_timer():
    with open(WIFI_DATA_PATH) as f:
        try:
            timer = float(f.readline().rstrip())
        except:
            return -1
    return timer

while get_timer() != 0:
    time.sleep(1/30)
    continue

x = dim[0] + round(dim[2] / 1.64)
y = dim[1] + round(dim[3] / 4.54)

y2 = dim[1] + round(dim[3] / 1.26)
pyautogui.moveTo(x,y2)
pyautogui.dragTo(x, y, duration=0.8)

time.sleep(3.5)