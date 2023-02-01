import time
from utility import *
from math import dist
import networkx as nx
from solver import *


def printConstantGameData():
    try:
        load_dict()
        while True:
            data = getGameData()
            if not data:
                continue
            for key in data.keys():
                print(data[key])
            for i in range(len(data["tasks"])):
                print(f"{data['tasks'][i]}: ", end='')
                print(get_task_position(data, i))
            print()
            time.sleep(2)

    except KeyboardInterrupt:
        pass


def printGameData():
    data = getGameData()
    load_dict()
    while not data:
        data = getGameData()
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

def move_and_complete_tasks(graph, move_list, tasks):
    G = generate_graph(graph)
    nearest = move_to_nearest_node(graph)
    move_list = sort_shortest_path(G, nearest, move_list, tasks)
    while len(move_list) > 0:
        move(list(nx.shortest_path(G, nearest, move_list[0], weight="weight")))
        tsk = get_nearest_task(tasks[0])
        return_code = solve_task(task_name=tsk[0])

        if return_code == 1:
            while in_meeting():
                time.sleep(1/60)
            nearest = move_to_nearest_node(graph)

            # Sort move list by distance
            move_list = sort_shortest_path(G, nearest, move_list, tasks)
            continue

        if len(move_list) == 0:
            break

        # Add next task step to move list, if any
        time.sleep(1/60)
        update_move_list(move_list, tasks, tsk[0])
        index = tasks[0].index(tsk[0])

        nearest = move_to_nearest_node(graph)

        # Sort move list by distance
        move_list = sort_shortest_path(G, nearest, move_list, tasks)

        # Remove completed task from tasks and move list
        for i in range(len(tasks)):
            tasks[i].pop(index) 
        move_list.pop(0)
        
if __name__ == "__main__":
    focus()
    graph = load_graph_list("SHIP")
    tasks = get_task_list()
    move_list = get_move_list(tasks)
    move_and_complete_tasks(graph, move_list, tasks)


