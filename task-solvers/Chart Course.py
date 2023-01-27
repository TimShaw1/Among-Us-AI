from task_utility import *
import time
import cv2
import copy

click_use()
time.sleep(0.8)

dimensions = get_dimensions()
dimensions[0] += round(dimensions[2] / 2.74)
dimensions[1] += round(dimensions[3] / 4.54)

s_dimensions = copy.deepcopy(dimensions)

s_dimensions[2] /= 2.51
s_dimensions[2] = round(s_dimensions[2])
s_dimensions[3] /= 1.83
s_dimensions[3] = round(s_dimensions[3])

print(s_dimensions)
get_screen_coords()

while not is_task_done("Chart Course"):
    screenshot = get_screenshot(s_dimensions)

    exit = False

    for x in range(screenshot.width):
        if not exit:
            for y in range(screenshot.height):
                pixel = screenshot.getpixel((x, y))
                if pixel[1] < 70 and pixel[1] > 50 and pixel[0] < 30 and pixel[0] > 10 and pixel[2] < 70:
                    pyautogui.click(dimensions[0] + x, dimensions[1] + y) 
                    exit = True
                    break
        else:
            break
    exit = False

# Color is 36 111 161