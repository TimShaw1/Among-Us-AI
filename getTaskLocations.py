import json
import time
import copy
from utility import *

# Check for changes in a list. Returns index of change
def check_changes(new_data, old_data):
    """Check for changes in a list.

        Returns
        --------
        int
            index of change

            -1 if nothing

            -2 if list changed (reset flag)
    """
    if new_data['tasks'] and old_data['tasks'] and data["status"]:
        # If new task, return index of last element
        if len(new_data['tasks']) > len(old_data['tasks']):
            return len(data['tasks']) - 1
    if new_data['task_steps'] and old_data['task_steps']:
        if len(new_data['task_steps']) != len(old_data['task_steps']):
            return -2
        for i in range(len(new_data['task_steps'])):
            if new_data['task_steps'][i] != old_data['task_steps'][i]:
                # If next task step, return index of task step
                if new_data['tasks'][i] == old_data['tasks'][i]:
                    return i
                else:
                    # return reset flag
                    return -2
    return -1

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

        # Reset
        if change_index == -2:
            old_data = copy.deepcopy(data)
            continue

        # Check for updated task steps -- fuel engines is broken
        if (change_index >= 0 and not data["dead"]):
            old_data["position"] = data["position"]
            update_current(data, change_index)
            old_data = copy.deepcopy(data)
            print()

        time.sleep(0.0166)

except KeyboardInterrupt:
    pass
