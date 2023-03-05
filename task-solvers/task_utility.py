from PIL import ImageGrab
import ctypes
import win32gui
import pyautogui
import numpy as np
import cv2
import os
import pydirectinput
from wake_keyboard import wake


ctypes.windll.user32.SetProcessDPIAware()

SEND_DATA_PATH = "sendData.txt"

def getGameData():
    x,y,status,tasks, task_locations, task_steps, map_id, dead = None, None, None, None, None, None, None, None
    with open(SEND_DATA_PATH) as file:
        lines = file.readlines()
        if len(lines) > 0:
            x = float(lines[0].split()[0])
            y = float(lines[0].split()[1])
            status = lines[1].strip()
            if len(lines) > 2:
                tasks = lines[2].rstrip().strip('][').split(", ")
            if len(lines) > 3:
                task_locations = lines[3].rstrip().strip('][').split(", ")
            if len(lines) > 4:
                task_steps = lines[4].rstrip().strip('][').split(", ")
            if len(lines) > 5:
                map_id = lines[5].rstrip()
            if len(lines) > 6:
                dead = bool(int(lines[6].rstrip()))

    return {"position" : (x,y), "status" : status, "tasks" : tasks, "task_locations" : task_locations, "task_steps" : task_steps, "map_id" : map_id, "dead": dead}

def get_screenshot(dimensions=None, window_title="Among Us"):
    if window_title:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd and not dimensions:
            win32gui.SetForegroundWindow(hwnd)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
            im = pyautogui.screenshot(region=(x, y, x1, y1))
            return im
        elif dimensions:
            im = pyautogui.screenshot(region=dimensions)
            return im
        else:
            print('Window not found!')
    else:
        im = pyautogui.screenshot()
        return im

def get_dimensions():
    window_title="Among Us"
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        x, y, x1, y1 = win32gui.GetClientRect(hwnd)
        x, y = win32gui.ClientToScreen(hwnd, (x, y))
        x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
        return[x,y,x1,y1]
    else:
        print('Window not found!')

def click_use():
    wake()
    dim = get_dimensions()
    pydirectinput.moveTo(dim[0] + dim[2] - round(dim[2] / 13), dim[1] + dim[3] - round(dim[3] / 7))
    pydirectinput.click()
    return

def get_dir():
    return os.getcwd()

def get_screen_coords():
    while True:
        print(pyautogui.position(), end='\r')

def is_task_done(task):
    data = getGameData()
    while not data["task_steps"]:
        data = getGameData()

    if task == "Reset Reactor":
        if "Reset Reactor" in data['tasks']:
            return False
        else: 
            return True
    index = data["tasks"].index(task)
    steps = data["task_steps"][index].split('/')
    return steps[0] == steps[1]

def is_urgent_task() -> str:
    data = getGameData()
    while not data["tasks"]:
        data = getGameData()

    urgent_tasks = ["Reset Reactor", "Restore Oxygen"]
    for task in urgent_tasks:
        if task in data['tasks']:
            return task
    return None