import time
from utility import *
from math import dist
import networkx as nx
from solver import *
from random import choice
import keyboard

inspect_sample_flag : bool = False

def printConstantGameData(G):
    """Debugging function to print data from getGameData every 2 seconds"""
    try:
        load_dict()
        while True:
            data = getGameData()
            for key in data.keys():
                print(data[key])
            #for i in range(len(data["tasks"])):
                #print(f"{data['tasks'][i]}: ", end='')
                #print(get_task_position(data, i))
            print(on_cams())
            print()
            time.sleep(2)

    except KeyboardInterrupt:
        pass


def printGameData():
    """Debugging function to print data from getGameData"""
    data = getGameData()
    load_dict()
    for key in data.keys():
        print(data[key])
    for i in range(len(data["tasks"])):
        print(f"{data['tasks'][i]}: ", end='')
        print(get_task_position(data, i))
    print()

def printConstantTaskPositions():
    """Debugging function to print task positions"""
    try:
        while True:
            data = getGameData()
            if not data:
                continue
            for i in range(len(data["tasks"])):
                print(f"{data['tasks'][i]}: ", end='')
                print(get_task_position(data, i))
            print()
            time.sleep(1)

    except KeyboardInterrupt:
        pass

def idle(G):
    """Player just runs to random task locations"""
    move_list = get_idle_list()
    can_vote_flag : bool = False
    while len(move_list) > 0:
        if not isInGame() or keyboard.is_pressed('`'):
            break
        nearest = move_to_nearest_node(graph)
        destination = choice(move_list)
        if "Fix Lights" in data["tasks"]:
            dict = load_dict()
            loc = "Electrical(10/-11)" if data["map_id"].upper() != "SHIP" else "Electrical"
            destination = tuple(dict["Fix Lights"][loc])
        urgent = is_urgent_task()
        if urgent is not None:
            dict = load_dict()
            destination = tuple(dict[urgent[0]][urgent[1]])
        move_return_code = move(list(nx.shortest_path(G, nearest, destination, weight="weight")), G)
        if isImpostor():
            solve_task(get_nearest_task()[0])
            urgent = is_urgent_task()
        if urgent is not None and move_return_code == 0:
            urgent = is_urgent_task()
            if urgent is not None:
                solve_task(urgent[0])
            nearest = move_to_nearest_node(graph)
            if urgent is not None and urgent[0] == "Restore Oxygen":
                if (is_urgent_task() is not None):
                    # TODO: Position is hard coded to skeld for now - fine for polus
                    move(list(nx.shortest_path(G, nearest, (6.521158, -7.138555), weight="weight")), G)
                    solve_task(task_name="Restore Oxygen", task_location="Admin")
                nearest = move_to_nearest_node(graph)
        if move_return_code == 1:
            chat(can_vote_flag)
            set_can_vote_false()
            can_vote_flag = False
            time.sleep(5)
            nearest = move_to_nearest_node(graph)
            continue

def move_and_complete_tasks(G, move_list, tasks):
    # Initialize flags
    global inspect_sample_flag
    can_vote_flag : bool = False

    # Find graph node closest to player (helps represent the game as a graph)
    nearest = move_to_nearest_node(graph)

    # Get list of destination coordinates
    move_list = sort_shortest_path(G, nearest, move_list, tasks)

    dead = isDead()

    # While we still have tasks to do
    while len(move_list) > 0:
        # exit case
        if not isInGame() or keyboard.is_pressed('`'):
            break

        # move to next task
        move_return_code = move(list(nx.shortest_path(G, nearest, move_list[0], weight="weight")), G)

        # if we died while moving, exit
        if dead != isDead():
            break

        # If we are in a meeting,
        if move_return_code == 1:
            # chat
            chat(can_vote_flag)
            set_can_vote_false()
            can_vote_flag = False
            time.sleep(5)

            # Move to nearest graph node and continue
            nearest = move_to_nearest_node(graph)
            continue
        tsk = get_nearest_task(tasks[0])

        # Issue is due do tsk being too high here - get_nearest_task
        if tsk[1] > 1.5:
            return -1

        # Inspect sample cases
        # If we did the first part, do the second
        if inspect_sample_flag and tsk[0] == "Inspect Sample":
            return_code = solve_task(task_name="Inspect Sample 2", task_location="Medbay")
        elif inspect_sample_flag and tsk[0] == "Reboot Wifi":
            return_code = solve_task(task_name="Reboot Wifi 2", task_location="Communications")
        else:
            return_code = solve_task(task_name=tsk[0], task_location=tsk[2])

        # If task not found, exit
        if return_code == -1:
            break

        # Restore Oxygen case
        if tsk[0] == "Restore Oxygen" and return_code == 0 and not isDead():
            nearest = move_to_nearest_node(graph)

            if is_urgent_task() is not None:
                # TODO: Position is hard coded to skeld for now - fine for polus
                move(list(nx.shortest_path(G, nearest, (6.521158, -7.138555), weight="weight")), G)
                return_code = solve_task(task_name="Restore Oxygen", task_location="Admin")
            nearest = move_to_nearest_node(graph)

            # Sort move list by distance
            move_list = sort_shortest_path(G, nearest, move_list, tasks)

            # Remove Restore Oxygen from move list
            move_list.pop(0)
            continue

        # Reset Reactor case
        if tsk[0] == "Reset Reactor" and return_code == 0 and not isDead():
            nearest = move_to_nearest_node(graph)

            # Sort move list by distance
            move_list = sort_shortest_path(G, nearest, move_list, tasks)

            # Remove Reset Reactor from move list
            move_list.pop(0)
            continue

        # If meeting was called (also include inspect sample case)
        if return_code == 1 or return_code == 2:
            # exit case
            if keyboard.is_pressed('`'):
                break

            if return_code == 2:
                inspect_sample_flag = True

            if in_meeting():
                chat(can_vote_flag)
                set_can_vote_false()
                can_vote_flag = False
                time.sleep(5)
            nearest = move_to_nearest_node(graph)

            # Sort move list by distance
            move_list = sort_shortest_path(G, nearest, move_list, tasks)
            if tsk[0] == "Reset Reactor" or tsk[0] == "Restore Oxygen":
                move_list.pop(0)
            if (tsk[0] == "Inspect Sample" or tsk[0] == "Reboot Wifi") and return_code == 2:
                temp = move_list[0]
                move_list.pop(0)
                move_list.append(temp)

            continue

        # If we're done all out tasks
        if len(move_list) == 0:
            break

        # Add next task step to move list, if any
        time.sleep(1/60)
        try:
            update_move_list(move_list, tasks, tsk[0])
            index = tasks[0].index(tsk[0])
        except ValueError:
            move_list.pop(0) # edit here
            nearest = move_to_nearest_node(graph)

            # Sort move list by distance
            move_list = sort_shortest_path(G, nearest, move_list, tasks)
            continue

        nearest = move_to_nearest_node(graph)

        # Sort move list by distance
        move_list = sort_shortest_path(G, nearest, move_list, tasks)

        # remove task we just did
        move_list.pop(0)

        # Remove completed task from tasks and move list
        for i in range(len(tasks)):
            try:
                tasks[i].pop(index) 
            except IndexError:
                continue
    return 0

def main(G) -> int:
    # Get tasks
    tasks = get_task_list()

    # Initialize places to move to
    move_list = get_move_list(tasks)

    set_can_vote_false()

    with open("last_task.txt", "w") as f:
        f.write("nothing. No tasks completed yet")
    f.close()

    room = getGameData()["room"]
    with open("last_area.txt", "w") as f:
        f.write(room)
    f.close()

    dead = isDead()

    idle(G)

    ret = 0
    while True:
        if isInGame() and not keyboard.is_pressed('`'):
            # Begin gameplay loop
            if not isImpostor():
                ret = move_and_complete_tasks(G, move_list, tasks)
            if dead != isDead() or ret == -1:
                return -1
            # Idly move around
            idle(G)
            if dead != isDead():
                return -1
        else:
            return 0

if __name__ == "__main__":
    # Focus app
    focus()

    # Clear previous chat data
    clear_chat()

    # Clear previous kill data
    clear_kill_data()

    data = getGameData()

    # Load map graph
    graph = load_graph_list(data["map_id"])

    G = generate_graph(graph)
    #G = load_G(data["map_id"])

    # Print
    print("The Among Us AI\nHold ` for 7 seconds to stop. Press ctrl+alt+del to forcibly stop a task.")

    while True:
        ret = main(G)
        if keyboard.is_pressed('`'):
            break
        if ret == -1:
            print("restarting main...")
            main(G)
        time.sleep(1/60)
