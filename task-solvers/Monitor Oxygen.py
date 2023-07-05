import time
from task_utility import *
import pyautogui
import asyncio

click_use()
time.sleep(0.3)

dim = get_dimensions()

x = dim[0] + round(dim[2] / 2.97)
y = dim[1] + round(dim[3] / 4.9)

x_offset = round(dim[2] / 7.93)
y_height = round(dim[3] / 2.15)

y_dests = [round(dim[3] / 1.78), round(dim[3] / 3.68), round(dim[3] / 1.5), round(dim[3] / 3)]

async def get_y_spots(i):
    # 126,196,220
    if is_urgent_task() is not None:
        raise SystemExit(0)
    for j in range(round(y_height / 4)):
        pixel = pyautogui.pixel(x + x_offset*i, y + 4*j)
        if abs(pixel[0] - 126) < 3 and abs(pixel[1] - 196) < 3 and abs(pixel[2] - 220) < 3:
            return [(x + x_offset*i, y + j*4), (x + x_offset*i, dim[1] + y_dests[i])]
        
async def main():
    res = await asyncio.gather(
        get_y_spots(0),
        get_y_spots(1),
        get_y_spots(2),
        get_y_spots(3)
    )

    for i in range(4):
        pyautogui.moveTo(res[i][0])
        pyautogui.mouseDown()
        pyautogui.moveTo(res[i][1], duration=0.5)
        pyautogui.mouseUp()

asyncio.run(main())