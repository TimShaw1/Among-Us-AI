import json
from math import atan2, sin, cos, dist
import vgamepad as vg
import time
import pickle
import networkx as nx
from datetime import datetime
import win32gui

SHIP_TASK_TYPES = {}

AIRSHIP_TASK_TYPES = {}

PB_TASK_TYPES = {}

HQ_TASK_TYPES = {}

UNUSED_TASKS = ["Reset Reactor", "Fix Lights", "Fix Communications", "Restore Oxygen", "Reset Seismic Stabilizers", "Get Biggol Sword", "Stop Charles"]

SEND_DATA_PATH = "sendData.txt"

MAP = "SHIP"

global gamepad
gamepad = vg.VX360Gamepad()

def write_graph_list(list, map_name):
    with open(f'graphs\{map_name}_graph.pkl', 'wb') as f:
        pickle.dump(list, f)
    
    print(f'Wrote to graphs\{map_name}_graph.pkl')

def load_graph_list(map_name):
    with open(f'graphs\{map_name}_graph.pkl', 'rb') as f:
        return pickle.load(f)

def getGameData():
    x,y,status,tasks, task_locations, task_steps, map_id, dead, inMeeting = None, None, None, None, None, None, None, None, None
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
            if len(lines) > 7:
                inMeeting = bool(int(lines[7].rstrip()))

    return {"position" : (x,y), "status" : status, "tasks" : tasks, "task_locations" : task_locations, "task_steps" : task_steps, "map_id" : map_id, "dead": dead, "inMeeting" : inMeeting}

def save_dict_file(dict_to_save, dict_name):
    print(f"saving {dict_name}...")
    with open(f'tasks-json\{dict_name}.json', 'w') as f:
        json.dump(dict_to_save, f)

def save_current():
    global SHIP_TASK_TYPES, AIRSHIP_TASK_TYPES, PB_TASK_TYPES, HQ_TASK_TYPES, MAP
    if MAP == "SHIP":
        save_dict_file(SHIP_TASK_TYPES, "SHIP_TASK_TYPES")
    elif MAP == "AIRSHIP":
        save_dict_file(AIRSHIP_TASK_TYPES, "AIRSHIP_TASK_TYPES")
    elif MAP == "PB":
        save_dict_file(PB_TASK_TYPES, "PB_TASK_TYPES")
    elif MAP == "HQ":
        save_dict_file(HQ_TASK_TYPES, "HQ_TASK_TYPES")

def update_tasks(dict_to_use, dict_name, data, i):
    if data["map_id"] and data["map_id"].upper() != MAP:
        raise ValueError(f"Wrong map name. \nThis map is: {data['map_id'].upper()}")
    if data["task_locations"][i] not in dict_to_use[data["tasks"][i]].keys():
        dict_to_use[data["tasks"][i]][data["task_locations"][i]] = data["position"]
        print(f"task: {data['tasks'][i]} location:{[data['task_locations'][i]]} position: {data['position']}")
        print(dict_to_use[data["tasks"][i]][data["task_locations"][i]])
        save_current()
    else:
        print("already have it")

def update_current(data, i):
    global SHIP_TASK_TYPES, AIRSHIP_TASK_TYPES, PB_TASK_TYPES, HQ_TASK_TYPES, MAP
    if data["map_id"] and data["map_id"].upper() != MAP:
        raise ValueError(f"Wrong map name. \nThis map is: {data['map_id'].upper()}")
    if MAP == "SHIP":
        update_tasks(SHIP_TASK_TYPES, "SHIP_TASK_TYPES", data, i)
    elif MAP == "AIRSHIP":
        update_tasks(AIRSHIP_TASK_TYPES, "AIRSHIP_TASK_TYPES", data, i)
    elif MAP == "PB":
        update_tasks(PB_TASK_TYPES, "PB_TASK_TYPES", data, i)
    elif MAP == "HQ":
        update_tasks(HQ_TASK_TYPES, "HQ_TASK_TYPES", data, i)
    return

def load_dict():
    global SHIP_TASK_TYPES, AIRSHIP_TASK_TYPES, PB_TASK_TYPES, HQ_TASK_TYPES, MAP
    if MAP == "SHIP":
        with open("tasks-json\SHIP_TASK_TYPES.json") as file:
            SHIP_TASK_TYPES = json.load(file)
            return SHIP_TASK_TYPES
    elif MAP == "AIRSHIP":
        with open("tasks-json\AIRSHIP_TASK_TYPES.json") as file:
            AIRSHIP_TASK_TYPES = json.load(file)
            return AIRSHIP_TASK_TYPES
    elif MAP == "PB":
        with open("tasks-json\PB_TASK_TYPES.json") as file:
            PB_TASK_TYPES = json.load(file)
            return PB_TASK_TYPES
    elif MAP == "HQ":
        with open("tasks-json\HQ_TASK_TYPES.json") as file:
            HQ_TASK_TYPES = json.load(file)
            return HQ_TASK_TYPES
    return

def is_task_done(task):
    data = getGameData()
    while not data["task_steps"]:
        data = getGameData()

    index = data["tasks"].index(task)
    steps = data["task_steps"][index].split('/')
    return steps[0] == steps[1]

# Returns the x and y coordinates of a task in a list
# accepts the game data and the index of the task
def get_task_position(data, i):
    global SHIP_TASK_TYPES, AIRSHIP_TASK_TYPES, PB_TASK_TYPES, HQ_TASK_TYPES, MAP
    if MAP == "SHIP":
        return SHIP_TASK_TYPES[data["tasks"][i]][data["task_locations"][i]]
    elif MAP == "AIRSHIP":
        return AIRSHIP_TASK_TYPES[data["tasks"][i]][data["task_locations"][i]]
    elif MAP == "PB":
        return PB_TASK_TYPES[data["tasks"][i]][data["task_locations"][i]]
    elif MAP == "HQ":
        return HQ_TASK_TYPES[data["tasks"][i]][data["task_locations"][i]]

def get_nearest_task(tasks):
    data = getGameData()
    while not data["position"][0]:
        data = getGameData()
    pos = data["position"]

    dict = load_dict()
    smallest_dist = 100
    nearest = ()

    for subdict in dict.keys():
        if subdict not in tasks:
            continue
        if is_task_done(subdict):
            continue
        index = data["tasks"].index(subdict)
        for location in dict[subdict].keys():
            if location != data["task_locations"][index]:
                continue
            d = dist(dict[subdict][location], pos)
            if d < smallest_dist:
                smallest_dist = d
                nearest = subdict
    return (nearest, smallest_dist)


def get_angle_radians(point1, point2):
    # atan2(y,x)
    return atan2(point2[1] - point1[1], point2[0] - point1[0])

# Return the x and y percentages the gamepad should be held at
def points_to_gamepad(point1, point2):
    angle = get_angle_radians(point1, point2)
    return (round(cos(angle), 5), round(sin(angle), 5))

def get_smallest_dist(graph, pos):
    smallest_dist = 100
    for item in graph:
        distance = dist(item, pos)
        if distance < smallest_dist:
            smallest_dist = distance
    return smallest_dist

def move_to_nearest_node(graph):
    data = getGameData()
    while not data["position"][0]:
        data = getGameData()
    pos = data["position"]

    smallest_dist = 100
    nearest = ()
    for item in graph:
        distance = dist(item, pos)
        if distance < smallest_dist:
            smallest_dist = distance
            nearest = item
    move([nearest])
    return nearest

def generate_graph(graph):

    dict = load_dict()

    G = nx.Graph()

    for point in graph:
        G.add_node(point)

    for subdict in dict.keys():
        for location in dict[subdict].keys():
            G.add_node(tuple(dict[subdict][location]))

    for point in G.nodes:
        for point2 in G.nodes:
            if dist(point, point2) < 1:
                if point != point2:
                    G.add_edge(point, point2, weight=round(dist(point, point2),4))

    return G

def sort_shortest_path(G, nearest, move_list, tasks):
    move_list.sort(key = lambda x:nx.shortest_path_length(G, nearest, x, weight="weight"))
    return move_list

def get_task_list():
    data = getGameData()
    while not data["task_steps"]:
        data = getGameData()

    return [data["tasks"], data["task_locations"], data["task_steps"]]

def get_move_list(tasks):
    move_list = []
    dict = load_dict()
    for i in range(len(tasks[0])):
        if not is_task_done(tasks[0][i]):
            move_list.append(tuple(dict[tasks[0][i]][tasks[1][i]]))

    return move_list

def update_move_list(move_list, old_tasks, tsk):
    tasks = get_task_list()
    dict = load_dict()
    task = tsk

    if len(old_tasks) == 0:
        return

    # Get progress of current task
    progress = tasks[2][tasks[0].index(task)].split("/")
    progress = [int(i) for i in progress]

    if tsk == "Divert Power" and old_tasks[1][old_tasks[0].index(tsk)] != "Electrical":
        progress[0] += 1

    # If task is incomplete, 
    if progress[0] < progress[1]:

        # Get correct index of updated task
        index = tasks[0].index(task)

        # Add next task step to move list
        move_list.append(tuple(dict[tasks[0][index]][tasks[1][index]]))

        # Add next task step to our old tasks
        for i in range(len(old_tasks)):
            old_tasks[i].append(tasks[i][index])
    
    return task

def in_meeting():
    data = getGameData()
    while not data["inMeeting"]:
        data = getGameData()

    return data["inMeeting"]
    
def focus():
    window_title="Among Us"
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(1/60)
    else:
        print("Window not found")

def move(dest_list):
    global gamepad

    data = getGameData()
    while not data["position"][0]:
        data = getGameData()

    pos = data["position"]
    old_pos = pos
    old_time = datetime.now().second

    while len(dest_list) > 0:
        #print('\r', end='')
        #print(f"Distance to destination: {round(dist(pos, dest_list[0]), 4)}", end='')

        if dist(pos, dest_list[0]) < 0.1:
            dest_list.pop(0)
            if (len(dest_list) <= 0):
                break
        else:
            g_points = points_to_gamepad(pos, dest_list[0])
            gamepad.left_joystick_float(x_value_float=g_points[0], y_value_float=g_points[1])
            gamepad.update()

        if round(pos[0] - old_pos[0], 4) != 0 or round(pos[1] - old_pos[1], 4) != 0:
            old_time = datetime.now().second
            old_pos = pos
        else:
            if abs(old_time - datetime.now().second) > 1 and abs(old_time - datetime.now().second) < 5:
                print("\nGetting unstuck...")
                g_points = points_to_gamepad(pos, dest_list[0])
                gamepad.left_joystick_float(x_value_float=g_points[0], y_value_float=0)
                gamepad.update()
                time.sleep(0.7)
                gamepad.left_joystick_float(x_value_float=0, y_value_float=g_points[1])
                gamepad.update()
                time.sleep(0.7)

        data = getGameData()
        while not data["position"][0]:
            data = getGameData()

        pos = data["position"]
        time.sleep(1/60)

    gamepad.reset()
    gamepad.update()
    return

