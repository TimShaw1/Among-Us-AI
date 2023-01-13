import json
import time
from utility import *

# Check for changes in a list
def check_changes(new_list, old_list):
    if new_list and old_list:
        for i in range(len(new_list)):
            if new_list[i] != old_list[i]:
                return i
    return -1

load_dict()

data = getGameData()
while not data["task_steps"]:
    data = getGameData()
old_list = data["task_steps"]
old_data = data

try:
    while True:
        data = getGameData()
        if not data:
            continue

        change_index = check_changes(data["task_steps"], old_list)

        # Check for updated task steps
        if (change_index != -1):
            old_data["position"] = data["position"]
            update_current(old_data, change_index)
            old_list = data["task_steps"]
            old_data = data
            print()

except KeyboardInterrupt:
    pass
