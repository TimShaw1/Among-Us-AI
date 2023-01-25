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

def move_test(graph, move_list, tasks):
    while len(move_list) > 0:
        nearest = move_to_nearest_node(graph)
        G = generate_graph(graph)
        move(list(nx.shortest_path(G, nearest, move_list[0], weight="weight")))
        solve_task(task_name=tasks[0][0])

        # Add next task step to move list, if any
        time.sleep(1/60)
        update_move_list(move_list, tasks)

        # Remove completed task from tasks and move list
        for i in range(len(tasks)):
            tasks[i].pop(0)
        move_list.pop(0)
        print(move_list)
        time.sleep(1)
        



if __name__ == "__main__":
    time.sleep(2)
    graph = get_graph_list("SHIP")
    tasks = get_task_list()
    move_list = get_move_list(tasks)
    move_test(graph, move_list, tasks)

# (-7.95224, 0.5086)


