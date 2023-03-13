import time
from utility import *
from math import dist
import networkx as nx
from solver import *
from random import choice

def printConstantGameData():
    try:
        load_dict()
        while True:
            data = getGameData()
            for key in data.keys():
                print(data[key])
            #for i in range(len(data["tasks"])):
                #print(f"{data['tasks'][i]}: ", end='')
                #print(get_task_position(data, i))
            print()
            time.sleep(2)

    except KeyboardInterrupt:
        pass


def printGameData():
    data = getGameData()
    load_dict()
    for key in data.keys():
        print(data[key])
    for i in range(len(data["tasks"])):
        print(f"{data['tasks'][i]}: ", end='')
        print(get_task_position(data, i))
    print()

def printConstantTaskPositions():
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

def idle(graph):
    G = generate_graph(graph)
    move_list = get_idle_list()
    can_vote_flag : bool = False
    while len(move_list) > 0:
        if not isInGame():
            break
        nearest = move_to_nearest_node(graph)
        destination = choice(move_list)
        urgent = is_urgent_task()
        if urgent is not None:
            dict = load_dict()
            destination = tuple(dict[urgent[0]][urgent[1]])
        move_return_code = move(list(nx.shortest_path(G, nearest, destination, weight="weight")))
        if urgent is not None and move_return_code == 0:
            urgent = is_urgent_task()
            solve_task(urgent[0])
            nearest = move_to_nearest_node(graph)
            if urgent[0] == "Restore Oxygen":
                move(list(nx.shortest_path(G, nearest, (6.521158, -7.138555), weight="weight")))
                solve_task(task_name="Restore Oxygen")
                nearest = move_to_nearest_node(graph)
        if move_return_code == 1:
            chat(can_vote_flag)
            set_can_vote_false()
            can_vote_flag = False
            time.sleep(5)
            nearest = move_to_nearest_node(graph)
            continue


def move_and_complete_tasks(graph, move_list, tasks):
    inspect_sample_flag : bool = False
    can_vote_flag : bool = False
    G = generate_graph(graph)
    nearest = move_to_nearest_node(graph)
    move_list = sort_shortest_path(G, nearest, move_list, tasks)
    while len(move_list) > 0:
        if not isInGame():
            break
        move_return_code = move(list(nx.shortest_path(G, nearest, move_list[0], weight="weight")))
        if move_return_code == 1:
            chat(can_vote_flag)
            set_can_vote_false()
            can_vote_flag = False
            time.sleep(5)
            nearest = move_to_nearest_node(graph)
            continue
        tsk = get_nearest_task(tasks[0])

        # Issue is due do tsk being too high here - get_nearest_task
        if tsk[1] > 1.5:
            print(tsk)
            print(move_list)
            print("ERROR")

        if inspect_sample_flag and tsk[0] == "Inspect Sample":
            return_code = solve_task(task_name="Inspect Sample 2", task_location="Medbay")
        else:
            return_code = solve_task(task_name=tsk[0], task_location=tsk[2])

        if return_code == -1:
            break

        if tsk[0] == "Restore Oxygen" and return_code == 0:
            nearest = move_to_nearest_node(graph)
            move(list(nx.shortest_path(G, nearest, (6.521158, -7.138555), weight="weight")))
            return_code = solve_task(task_name="Restore Oxygen", task_location="Admin")
            nearest = move_to_nearest_node(graph)

            # Sort move list by distance
            move_list = sort_shortest_path(G, nearest, move_list, tasks)

            # Remove Restore Oxygen from move list
            move_list.pop(0)
            continue

        if tsk[0] == "Reset Reactor" and return_code == 0:
            nearest = move_to_nearest_node(graph)

            # Sort move list by distance
            move_list = sort_shortest_path(G, nearest, move_list, tasks)

            # Remove Reset Reactor from move list
            move_list.pop(0)
            continue

        if return_code == 1 or return_code == 2:
            if return_code == 2:
                inspect_sample_flag = True
            chat(can_vote_flag)
            set_can_vote_false()
            can_vote_flag = False
            time.sleep(5)
            nearest = move_to_nearest_node(graph)

            # Sort move list by distance
            move_list = sort_shortest_path(G, nearest, move_list, tasks)
            if tsk[0] == "Reset Reactor" or tsk[0] == "Restore Oxygen":
                move_list.pop(0)
            continue

        if len(move_list) == 0:
            break

        # Add next task step to move list, if any
        time.sleep(1/60)
        try:
            update_move_list(move_list, tasks, tsk[0])
            index = tasks[0].index(tsk[0])
        except ValueError:
            nearest = move_to_nearest_node(graph)

            # Sort move list by distance
            move_list = sort_shortest_path(G, nearest, move_list, tasks)
            continue

        nearest = move_to_nearest_node(graph)

        # Sort move list by distance
        move_list = sort_shortest_path(G, nearest, move_list, tasks)

        move_list.pop(0)

        # Remove completed task from tasks and move list
        for i in range(len(tasks)):
            try:
                tasks[i].pop(index) 
            except IndexError:
                continue
        
if __name__ == "__main__":
    # Focus app
    focus()

    # Clear previous chat data
    clear_chat()

    # Load map graph
    graph = load_graph_list("SHIP")

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

    while True:
        if isInGame():
            # Begin gameplay loop
            move_and_complete_tasks(graph, move_list, tasks)

            # Idly move around
            idle(graph)
        # Click Continue
        # Click Play Again
        time.sleep(5)


