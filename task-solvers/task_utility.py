from PIL import ImageGrab
import ctypes
import win32gui
import pyautogui
import numpy as np
import cv2

ctypes.windll.user32.SetProcessDPIAware()

def get_screenshot(window_title="Among Us"):
    if window_title:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
            im = pyautogui.screenshot(region=(x, y, x1, y1))
            return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        else:
            print('Window not found!')
    else:
        im = pyautogui.screenshot()
        return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
