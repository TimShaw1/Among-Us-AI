from task_utility import *
import time
import pyautogui
import copy
import collections

click_use()
time.sleep(0.3)

dim = get_dimensions()

x = dim[0] + round(dim[2] / 4.24)
y = dim[1] + round(dim[3] / 3.28)

x_offset = round(dim[2] / 34)
y_offset = round(dim[3] / 19.82)

# path color = 165,162,140
# block color = 115,112,99
# start color = 255, 255, 255
def get_maze() -> list[list]:
    maze = []
    for i in range(19):
        maze.append([])
        for j in range(7):
            maze[i].append([])
            pixel = pyautogui.pixel(x + x_offset*i, y + y_offset*j)
            if (pixel[0] == 165 and pixel[1] == 162 and pixel[2] == 140) or (pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255):
                maze[i][j] = 0
            else:
                maze[i][j] = 1
    return maze

maze = get_maze()
maze[17][6] = 9
m = copy.deepcopy(maze)
wall, clear, goal = 0, 1, 9
width, height = 18, 7

def bfs(maze, start):
    print(len(maze))
    queue = collections.deque()
    queue.append(start)
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path
        if maze[y][x] == goal:
            return True
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)): #directions
            if ( 0 <= x2 < width and  0 <= y2 < height):
                if maze[y2][x2] != wall and (x2, y2) not in seen: 
                    queue.append( (x2, y2))
                    seen.add((x2, y2))
    return False

print(bfs(maze, (1,0)))