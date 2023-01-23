import numpy as np
import cv2
from task_utility import *
import os

template = cv2.imread("C:\\projects\\AmongUs\\Among-Us-AI\\task-solvers\\cv2-templates\\Align Engine Output\\Arrow.png", 0)
template = cv2.cvtColor(template, cv2.COLOR_RGBA2BGR)

screenshot = get_screenshot()

print(template.shape[:-1])
h,w  = template.shape[:-1]

# Perform match operations.
res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
  
# Specify a threshold
threshold = 0.6
  
# Store the coordinates of matched area in a numpy array
loc = np.where(res >= threshold)

# Draw a rectangle around the matched region.
for pt in zip(*loc[::-1]):
    cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
  
# Show the final image with the matched area.
cv2.imshow('Detected', screenshot)
cv2.waitKey(4000)