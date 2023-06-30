import time
from task_utility import *
import pyautogui

click_use()
time.sleep(0.3)

dim = get_dimensions()

skull_x = dim[0] + round(dim[2] / 4.025)
skull_y = dim[1] + round(dim[3] / 3.64)

skull_x2 = dim[0] + round(dim[2] / 2.26)
skull_y2 = dim[1] + round(dim[3] / 3.51)

crystal_x = dim[0] + round(dim[2] / 3.75)
crystal_y = dim[1] + round(dim[3] / 2.48)

crystal_x2 = dim[0] + round(dim[2] / 1.83)
crystal_y2 = dim[1] + round(dim[3] / 2.62)

leaf_x = dim[0] + round(dim[2] / 3.87)
leaf_y = dim[1] + round(dim[3] / 1.77)

leaf_x2 = dim[0] + round(dim[2] / 2.24)
leaf_y2 = dim[1] + round(dim[3] / 1.83)

gem_x = dim[0] + round(dim[2] / 3.95)
gem_y = dim[1] + round(dim[3] / 1.49)

gem_x2 = dim[0] + round(dim[2] / 1.83)
gem_y2 = dim[1] + round(dim[3] / 1.48)

pyautogui.moveTo(skull_x, skull_y)
pyautogui.dragTo(skull_x2, skull_y2, 0.8)

pyautogui.moveTo(crystal_x, crystal_y)
pyautogui.dragTo(crystal_x2, crystal_y2, 1)

pyautogui.moveTo(leaf_x, leaf_y)
pyautogui.dragTo(leaf_x2, leaf_y2, 0.8)

pyautogui.moveTo(gem_x, gem_y)
pyautogui.dragTo(gem_x2, gem_y2, 1)