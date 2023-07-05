from task_utility import *
import time
import pyautogui
import copy
import collections
import numpy

click_use()
time.sleep(0.3)

# color = 121,143,148
data = getGameData()
dim = get_dimensions()
if data["room"] == "Laboratory":
    if is_urgent_task() is not None:
        raise SystemExit(0)
    x = dim[0] + round(dim[2] / 3.5)
    y = dim[1] + round(dim[3] / 6.97)

    y_offset = round(dim[3] / 6.97)

    for i in range(6):
        pixel = pyautogui.pixel(x, y + y_offset*i)
        if max(abs(numpy.subtract(pixel, (121, 143, 148)))) < 3:
            pyautogui.click(x, y + y_offset*i)
            raise SystemExit(0)

x = dim[0] + round(dim[2] / 4.24)
y = dim[1] + round(dim[3] / 3.28)

x_offset = round(dim[2] / 34)
y_offset = round(dim[3] / 19.82)

# path color = 165,162,140 or 205,203,191
# block color = 115,112,99 or 77,76,66
# start color = 255, 255, 255
def get_maze() -> list[list]:
    maze = []
    for i in range(7):
        maze.append([])
        for j in range(19):
            maze[i].append([])
            pixel = pyautogui.pixel(x + x_offset*j, y + y_offset*i)
            if max(abs(numpy.subtract(pixel, (165, 162, 140)))) < 3 or max(abs(numpy.subtract(pixel, (255, 255, 255)))) < 3 or max(abs(numpy.subtract(pixel, (205, 203, 191)))) < 3:
                maze[i][j] = 0
            else:
                maze[i][j] = 1
        if is_urgent_task() is not None:
            raise SystemExit(0)
    return maze

maze = get_maze()

sol = []
dest = (17, 6)
start = (1, 0)

def search(maze, x, y, seen = []):
    sol.append((x,y))
    if (x,y) == dest:
        return True
    res = False
    if (x+1 < 19) and maze[y][x] == 0 and (x+1,y) not in seen:
        seen.append((x+1,y))
        res = search(maze, x+1, y, seen)
    if res == False and (y+1 < 7) and maze[y][x] == 0 and (x,y+1) not in seen:
        seen.append((x,y+1))
        res = search(maze, x, y+1, seen)
    if res == False and (x-1 >0) and maze[y][x] == 0 and (x-1,y) not in seen:
        seen.append((x-1,y))
        res = search(maze, x-1, y, seen)
    if res == False and (y-1 > 0) and maze[y][x] == 0 and (x,y-1) not in seen:
        seen.append((x,y-1))
        res = search(maze, x, y-1, seen)
    if res == False:
        sol.remove((x,y))
    return res

search(maze, 1, 0)
pyautogui.moveTo(x + x_offset*sol[0][0], y + y_offset*sol[0][1])
sol.pop(0)
pyautogui.mouseDown()
for point in sol:
    pyautogui.moveTo(x + x_offset*point[0], y + y_offset*point[1])
pyautogui.mouseUp()
