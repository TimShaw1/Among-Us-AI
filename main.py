import time
from utility import *
from math import dist
import networkx as nx


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

def move_test(graph, move_list):
    for destination in move_list:
        nearest = move_to_nearest_node(graph)
        G = generate_graph(graph)
        move(list(nx.shortest_path(G, nearest, destination, weight="weight")))
        time.sleep(1)

if __name__ == "__main__":
    time.sleep(2)
    graph = get_graph_list("SHIP")
    tasks = get_task_list()
    move_list = []
    dict = load_dict()
    for i in range(len(tasks[0])):
        move_list.append(tuple(dict[tasks[0][i]][tasks[1][i]]))
    move_test(graph, move_list)

# (-7.95224, 0.5086)


