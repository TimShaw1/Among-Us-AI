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
        load_dict()
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

def move_test(graph):
    nearest = move_to_nearest_node(graph)
    G = nx.Graph()

    for point in graph:
        G.add_node(point)

    for point in graph:
        for point2 in graph:
            if dist(point, point2) < 0.8:
                if point != point2:
                    G.add_edge(point, point2)
    nodes = list(G.nodes())
    move(list(nx.shortest_path(G, nearest, nodes[20])))

if __name__ == "__main__":
    time.sleep(2)
    graph = get_graph_list("SHIP")
    move_test(graph)

# (-7.95224, 0.5086)


