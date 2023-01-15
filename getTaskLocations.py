import json
import time
import copy
from utility import *

# Check for changes in a list
def check_changes(new_data, old_data):
    if new_data['task_steps'] and old_data['task_steps']:
        if len(new_data['task_steps']) != len(old_data['task_steps']):
            return -2
        for i in range(len(new_data['task_steps'])):
            if new_data['task_steps'][i] != old_data['task_steps'][i]:
                if new_data['tasks'][i] == old_data['tasks'][i]:
                    return i
                else:
                    return -2
    return -1

data = getGameData()
while not data["task_steps"]:
    data = getGameData()
old_data = copy.deepcopy(data)

load_dict()

try:
    while True:
        data = getGameData()
        if not data:
            continue

        if data["map_id"]:
            MAP = data["map_id"].upper()

        change_index = check_changes(data, old_data)

        if change_index == -2:
            old_data = copy.deepcopy(data)
            continue

        # Check for updated task steps
        if (change_index >= 0 and not data["dead"]):
            old_data["position"] = data["position"]
            update_current(old_data, change_index)
            old_data = copy.deepcopy(data)
            print()

except KeyboardInterrupt:
    pass
