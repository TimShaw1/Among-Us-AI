from task_utility import *
import time
import cv2
import copy

click_use()
time.sleep(0.8)

dimensions = get_dimensions()

s_dimensions = copy.deepcopy(dimensions)

s_dimensions[0] += round(dimensions[2] / 4)
s_dimensions[1] += round(dimensions[3] / 4)

s_dimensions[2] /= 2
s_dimensions[2] = round(s_dimensions[2])
s_dimensions[3] /= 2.01
s_dimensions[3] = round(s_dimensions[3])

x_points = [round(dimensions[2] / 6.78) + s_dimensions[0], 
            round(dimensions[2] / 4) + s_dimensions[0], 
            round(dimensions[2] / 2.84) + s_dimensions[0], 
            round(dimensions[2] / 2.2) + s_dimensions[0]]

ship_x = round(dimensions[2] / 22.33) + s_dimensions[0]

screenshot = get_screenshot(s_dimensions)

exit = False

for x in range(ship_x, ship_x+40):
    if not exit:
        for y in range(screenshot.height):
            pixel = screenshot.getpixel((x - s_dimensions[0], y))

            if pixel[0] < 47 and pixel[0] > 41 and pixel[1] < 120 and pixel[1] > 110 and pixel[2] < 165 and pixel[2] > 159:
                pyautogui.moveTo(x, s_dimensions[1] + y)
                exit = True
                break
    else:
        break

exit = False
y_offset = 15

while not is_task_done("Chart Course"):
    screenshot = get_screenshot(s_dimensions)

    for i in range(len(x_points)):
        for y in range(screenshot.height):
            pixel = screenshot.getpixel((x_points[i] - s_dimensions[0], y))
            if pixel[0] < 38 and pixel[0] > 32 and pixel[1] < 113 and pixel[1] > 108 and pixel[2] < 163 and pixel[2] > 158:
                if i == 3:
                    y_offset = 30
                pyautogui.dragTo(x_points[i] + 15, s_dimensions[1] + y + y_offset, duration=0.2, tween=pyautogui.easeOutQuad)
                break

# Color is 36 111 161
# Ship Color is 37 111 159