from task_utility import *
import time
import cv2
import pyautogui

click_use()
time.sleep(0.8)

dimensions = get_dimensions()

dimensions[0] += round(dimensions[2] / 1.56)
dimensions[2] = 2

yellow_offset = round(dimensions[3] / 4.8)
blue_offset = round(dimensions[3] / 2.16)
cyan_offset = round(dimensions[3] / 1.44)

button_offset = dimensions[3] / 14.4

# Green and Red > 200, Blue < 5 -- yellow

# 105 > Green and red > 80, blue > 250 -- blue

# 115 > R > 105, 255 > G > 245, B > 250

done = [False, False, False]

while not is_task_done(task="Calibrate Distributor"):
    screenshot = get_screenshot(dimensions)
    s_y = screenshot.getpixel((0, yellow_offset))
    s_b = screenshot.getpixel((0, blue_offset))
    s_c = screenshot.getpixel((0, cyan_offset))

    if s_y[0] < 5:
        done = [False, False, False]

    # Yellow check
    if done[0] == False:
        if s_y[0] > 200 and s_y[1] > 200 and s_y[2] < 5:
            pyautogui.click((dimensions[0], dimensions[1] + yellow_offset + button_offset))
            done[0] = True
        else:
            continue

    # Blue Check
    if done[1] == False:
        # Why did I write this like this lmao
        if s_b[0] < 105 and s_b[0] > 80 and s_b[1] < 105 and s_b[1] > 80 and s_b[2] > 250:
            pyautogui.click((dimensions[0], dimensions[1] + blue_offset + button_offset))
            done[1] = True
        else:
            continue

    # Cyan check
    if done[2] == False:
        if s_c[0] < 115 and s_c[0] > 105 and s_c[1] < 255 and s_c[1] > 245 and s_c[2] > 250:
            pyautogui.click((dimensions[0], dimensions[1] + cyan_offset + button_offset))
            done[2] = True
        else:
            continue