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