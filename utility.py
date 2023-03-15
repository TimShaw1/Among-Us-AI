import json
from math import atan2, sin, cos, dist
import vgamepad as vg
import time
import pickle
import networkx as nx
from datetime import datetime
import win32gui
import pyautogui
import matplotlib.pyplot as plt

SHIP_TASK_TYPES = {}

AIRSHIP_TASK_TYPES = {}

PB_TASK_TYPES = {}

HQ_TASK_TYPES = {}

UNUSED_TASKS = ["Reset Seismic Stabilizers", "Get Biggol Sword", "Stop Charles"]
SABOTAGE_TASKS = ["Reset Reactor", "Fix Lights", "Fix Communications", "Restore Oxygen"]

with open("sendDataDir.txt") as f:
    line = f.readline().rstrip()
    SEND_DATA_PATH = line + "\\sendData.txt"
    CHAT_DATA_PATH = line + "\\chatData.txt"
    CAN_VOTE_PATH = line + "\\canVote.txt"
    IN_GAME_PATH = line + "\\inGameData.txt"

MAP = "SHIP"

global gamepad
gamepad = vg.VX360Gamepad()

global impostor 
impostor = False

# save the current map's graph
def write_graph_list(list, map_name):
    with open(f'graphs\{map_name}_graph.pkl', 'wb') as f:
        pickle.dump(list, f)
    
    print(f'Wrote to graphs\{map_name}_graph.pkl')

# load the given map's graph 
def load_graph_list(map_name):
    with open(f'graphs\{map_name}_graph.pkl', 'rb') as f:
        return pickle.load(f)

# reads sendData.txt and parses data.
# Returns a dict containing all the data
def getGameData():
    global impostor

    # number of parameters (lines) in data
    dataLen : int = 13
    x,y,status,tasks, task_locations, task_steps, map_id, dead, inMeeting, speed, color, room, lights, nearbyPlayers = (None,)*(dataLen + 1) # x and y are 1 line, so add 1
    lines = []
    while True:
        with open(SEND_DATA_PATH) as file:
            lines = file.readlines()
            if len(lines) < dataLen:
                file.close()
                continue

            x = float(lines[0].split()[0])
            y = float(lines[0].split()[1])
            status = lines[1].strip()
            impostor = status

            tasks = lines[2].rstrip().strip('][').split(", ")

            task_locations = lines[3].rstrip().strip('][').split(", ")

            task_steps = lines[4].rstrip().strip('][').split(", ")

            map_id = lines[5].rstrip()

            dead = bool(int(lines[6].rstrip()))

            inMeeting = bool(int(lines[7].rstrip()))

            speed = float(lines[8].rstrip())

            color = translatePlayerColorID(int(lines[9].rstrip()))

            room = lines[10].rstrip()

            lights = False if '0' in lines[11].rstrip() else True

            nearbyPlayers = {}
            try:
                bigLongInput = lines[12].rstrip().strip('][').split(", ")
                for item in bigLongInput:
                    item = item.split("/")
                    nearbyPlayers[translatePlayerColorID(int(item[0]))] = (float(item[1]), float(item[2]))
            except ValueError:
                nearbyPlayers = []
        if None in [x,y,status,tasks, task_locations, task_steps, map_id, dead, inMeeting, speed, color, room, nearbyPlayers]:
            continue
        break

    if status == "impostor" and tasks is not None and task_locations is not None:
        if tasks[0] == "Submit Scan" and task_locations[0] == "Hallway":
            tasks.pop(0)
            task_locations.pop(0)
    return {"position" : (x,y), "status" : status, "tasks" : tasks, 
            "task_locations" : task_locations, "task_steps" : task_steps, 
            "map_id" : map_id, "dead": dead, "inMeeting" : inMeeting, 
            "speed" : speed, "color" : color, "room" : room, "lights" : lights, "nearbyPlayers" : nearbyPlayers}

def get_chat_messages() -> list:
    with open(CHAT_DATA_PATH) as file:
        lines = file.readlines()
        return [x.rstrip() for x in lines]

def translatePlayerColorID(id : int):
    col_array = ["RED", "BLUE", "GREEN", "PINK",
                "ORANGE", "YELLOW", "BLACK", "WHITE",
                "PURPLE", "BROWN", "CYAN", "LIME",
                "MAROON", "ROSE", "BANANA", "GRAY",
                "TAN", "CORAL"]
    
    return col_array[id]

# Saves the given coordinate dictionary dict_to_save to a json file named dict_name
def save_dict_file(dict_to_save, dict_name):
    print(f"saving {dict_name}...")
    with open(f'tasks-json\{dict_name}.json', 'w') as f:
        json.dump(dict_to_save, f)

# Saves the current coordinate dictionary using save_dict_file
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

# Updates the dictionary of graph coordinates for the given map (specified in dict_name)
def update_tasks(dict_to_use, dict_name, data, i):
    if data["map_id"] and data["map_id"].upper() != MAP:
        raise ValueError(f"Wrong map name. \nThis map is: {data['map_id'].upper()}")
    
    if data["tasks"][i] not in dict_to_use:
        dict_to_use[data["tasks"][i]] = {}

    if data["task_locations"][i] not in dict_to_use[data["tasks"][i]].keys():
        dict_to_use[data["tasks"][i]][data["task_locations"][i]] = data["position"]
        print(f"task: {data['tasks'][i]} location:{[data['task_locations'][i]]} position: {data['position']}")
        print(dict_to_use[data["tasks"][i]][data["task_locations"][i]])
        save_current()
    else:
        print("already have it")

# Helper function to call update_tasks
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

# Loads the current map's coordinate dictionary and 
# returns a dict object containing the task coordinate data.
def load_dict():
    global SHIP_TASK_TYPES, AIRSHIP_TASK_TYPES, PB_TASK_TYPES, HQ_TASK_TYPES, MAP
    if MAP == "SHIP":
        if SHIP_TASK_TYPES == {}:
            with open("tasks-json\SHIP_TASK_TYPES.json") as file:
                SHIP_TASK_TYPES = json.load(file)
                return SHIP_TASK_TYPES
        else:
            return SHIP_TASK_TYPES
        
    elif MAP == "AIRSHIP":
        if AIRSHIP_TASK_TYPES == {}:
            with open("tasks-json\AIRSHIP_TASK_TYPES.json") as file:
                AIRSHIP_TASK_TYPES = json.load(file)
                return AIRSHIP_TASK_TYPES
        else:
            return AIRSHIP_TASK_TYPES
        
    elif MAP == "PB":
        if PB_TASK_TYPES == {}:
            with open("tasks-json\PB_TASK_TYPES.json") as file:
                PB_TASK_TYPES = json.load(file)
                return PB_TASK_TYPES
        else:
            return PB_TASK_TYPES
        
    elif MAP == "HQ":
        if HQ_TASK_TYPES == {}:
            with open("tasks-json\HQ_TASK_TYPES.json") as file:
                HQ_TASK_TYPES = json.load(file)
                return HQ_TASK_TYPES
        else:
            return HQ_TASK_TYPES
    return

# Determines if a task is complete and returns True/False.
# If task is not found, returns True
def is_task_done(task):
    data = getGameData()

    try:
        if task in SABOTAGE_TASKS:
            if task in data["tasks"]:
                return False
            return True
            
        index = data["tasks"].index(task)
        steps = data["task_steps"][index].split('/')
        return steps[0] == steps[1]
    except (IndexError, ValueError):
        return True
    
def is_urgent_task(tasks : list = None) -> str:
    if tasks is None:
        data = getGameData()
        tasks = data['tasks']

    urgent_tasks = [("Reset Reactor", "Reactor"), ("Restore Oxygen", "Oxygen")]
    for task in urgent_tasks:
        if task[0] in tasks:
            return task
    return None

def can_vote() -> bool:
    with open(CAN_VOTE_PATH) as f:
        lines = f.readlines()
        canVote = False if '0' in  lines else True
    return canVote

def set_can_vote_false() -> None:
    with open(CAN_VOTE_PATH, "w") as f:
        f.write("0")

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

# Returns a tuple with (nearest task, dist to task) as parameters
def get_nearest_task(tasks):
    data = getGameData()
    pos = data["position"]

    dict1 = load_dict()
    smallest_dist = 100
    nearest = ()
    loc = ""

    tasks = data['tasks']

    # Loop through task names
    for subdict in dict1.keys():

        # Check for irrelevant data
        if subdict not in tasks and subdict not in SABOTAGE_TASKS:
            continue
        try:
            index = data["tasks"].index(subdict)
        except ValueError:
            index = -1

        # Loop through coordinates in dict at current location
        for location in dict1[subdict].keys():
            if subdict in SABOTAGE_TASKS and index == -1:
                d = dist(dict1[subdict][location], pos)
                if d < smallest_dist and d < 1.5:
                    smallest_dist = d
                    nearest = subdict
                    loc = location
                    continue
            
            # Check for correct task but wrong location
            if location != data["task_locations"][index]:
                continue

            # Calculate distance and determine if it is the smallest
            d = dist(dict1[subdict][location], pos)
            if d < smallest_dist:
                smallest_dist = d
                nearest = subdict
                loc = location

    return (nearest, smallest_dist, loc)

def get_nearby_players(G):
    players = getGameData()["nearbyPlayers"]
    near_players = []
    for player in players.keys():
        if get_real_dist(G,  players[player]) < 5.5:
            near_players.append(player)
    return near_players

# converts 2 points to an angle in radians
def get_angle_radians(point1, point2):
    # atan2(y,x)
    return atan2(point2[1] - point1[1], point2[0] - point1[0])

# Return the x and y percentages the gamepad should be held at
def points_to_gamepad(point1, point2):
    angle = get_angle_radians(point1, point2)
    return (round(cos(angle), 5), round(sin(angle), 5))

# returns the smallest dist from pos to the nearest node on the graph
def get_smallest_dist(graph, pos):
    smallest_dist = 100
    for item in graph:
        distance = dist(item, pos)
        if distance < smallest_dist:
            smallest_dist = distance
    return smallest_dist

# moves the player to the nearest node on the graph
def move_to_nearest_node(graph):
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

def get_nearest_node(G : nx.Graph, node_pos : tuple):
    smallest_dist = 100
    nearest = ()
    for item in G.nodes.items():
        distance = dist(item[0], node_pos)
        if distance < smallest_dist:
            smallest_dist = distance
            nearest = item[0]
    return nearest

def get_real_dist(G : nx.Graph, node_pos : tuple) -> tuple:

    node_pos = get_nearest_node(G, node_pos)

    data = getGameData()
    pos = get_nearest_node(G, data["position"])

    distance = nx.shortest_path_length(G, pos, node_pos, weight="weight")
    return distance

# Creates a graph and adds nodes and edges between (if distance is great enough)
def generate_graph(graph):

    dict = load_dict()

    G = nx.Graph()

    for point in graph:
        G.add_node(point)

    for subdict in dict.keys():
        for location in dict[subdict].keys():
            G.add_node(tuple(dict[subdict][location]))

    G.add_node(tuple((6.521158, -7.138555)))

    for point in G.nodes:
        for point2 in G.nodes:
            if dist(point, point2) < 1:
                if point != point2:
                    G.add_edge(point, point2, weight=round(dist(point, point2),4))
    
    return G

def show_graph(G : nx.Graph, graph : list):
    options = {
    "font_size": 36,
    "node_size": 60,
    "node_color": "white",
    "edgecolors": "black",
    "linewidths": 3,
    "width": 3,
    }
    ax = plt.gca()
    pos = {n: n for n,x in G.nodes.data()}
    nx.draw(G, pos=pos, **options)
    # Set margins for the axes so that nodes aren't clipped
    ax.margins(0.10)
    plt.axis("off")
    plt.show()

# Sorts the move list in ascending order in terms of 
# distance from the player to the destination
def sort_shortest_path(G, nearest, move_list, tasks):
    move_list.sort(key = lambda x:nx.shortest_path_length(G, nearest, x, weight="weight"))
    urgent = is_urgent_task()
    if urgent is not None and not isDead():
        dict = load_dict()
        item = tuple(dict[urgent[0]][urgent[1]])
        if item in move_list:
            move_list.remove(item)
        move_list.insert(0, item)
    return move_list

# Gets task list from game data
def get_task_list():
    data = getGameData()

    return [data["tasks"], data["task_locations"], data["task_steps"]]

# Generates a list of destination coordinates
def get_move_list(tasks):
    move_list = []
    dict = load_dict()
    for i in range(len(tasks[0])):
        if not is_task_done(tasks[0][i]):
            try:
                move_list.append(tuple(dict[tasks[0][i]][tasks[1][i]]))
            except KeyError:
                continue

    return move_list

def get_idle_list():
    move_list = []
    dict = load_dict()
    for task in dict.keys():
        for location in dict[task].keys():
            move_list.append(tuple(dict[task][location]))
    return move_list


# Updates the move list
def update_move_list(move_list, old_tasks, tsk):

    if isImpostor():
        return

    tasks = get_task_list()
    dict = load_dict()
    task = tsk
    urgent_tasks = ["Reset Reactor", "Restore Oxygen"]

    if len(old_tasks) == 0:
        return
    
    for task1 in urgent_tasks:
        if task1 in tasks[0] and not isDead():
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

# Checks if we are in a meeting
def in_meeting() -> bool:
    data = getGameData()

    return data["inMeeting"]

def isImpostor() -> bool:
    return impostor == "impostor"

def isDead() -> bool:
    data = getGameData()
    return data['dead']

def isInGame() -> bool:
    with open(IN_GAME_PATH) as f:
        lines = f.readlines()
        inGame = False if '0' in lines else True
    return inGame

def allTasksDone() -> bool:
    data = getGameData()
    tasks = data["tasks"]
    for task in tasks:
        if not is_task_done(task):
            return False
    return True

def check_report():
    #220 37 0
    while True:
        print(pyautogui.position())

def clear_chat():
    open(CHAT_DATA_PATH, "w").close()
    
# focuses the among us window
def focus():
    window_title="Among Us"
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(1/60)
    else:
        print("Window not found")

# handles player movement
# Returns 0 on success, 1 if interrupted by a meeting
def move(dest_list) -> int:
    global gamepad

    data = getGameData()

    pos = data["position"]
    old_pos = pos
    old_time = datetime.now().second

    old_room = "None"

    while len(dest_list) > 0:
        if in_meeting():
            gamepad.reset()
            gamepad.update()
            return 1

        increment = 0.1
        if data['speed'] is not None:
            increment *= data['speed'] * 2
        if dist(pos, dest_list[0]) < increment:

            # Write last room visited
            room = getGameData()["room"]
            if room != old_room and room != "None" and room != "Hallway":
                with open("last_area.txt", "w") as f:
                    f.write(room)
                f.close()
                old_room = room

            dest_list.pop(0)
            if (len(dest_list) <= 0):
                break
        else:
            g_points = points_to_gamepad(pos, dest_list[0])
            gamepad.left_joystick_float(x_value_float=g_points[0], y_value_float=g_points[1])
            gamepad.update()

        # Check if stuck
        if round(pos[0] - old_pos[0], 4) != 0 or round(pos[1] - old_pos[1], 4) != 0:
            old_time = datetime.now().second
            old_pos = pos
        else:
            if abs(old_time - datetime.now().second) > 1 and abs(old_time - datetime.now().second) < 5:
                g_points = points_to_gamepad(pos, dest_list[0])
                gamepad.left_joystick_float(x_value_float=g_points[0], y_value_float=0)
                gamepad.update()
                time.sleep(0.3)
                gamepad.left_joystick_float(x_value_float=0, y_value_float=g_points[1])
                gamepad.update()
                time.sleep(0.3)

        data = getGameData()

        pos = data["position"]
        time.sleep(1/60)

    gamepad.reset()
    gamepad.update()
    return 0

