from utility import getGameData, load_graph_list, get_smallest_dist, write_graph_list, show_graph
import keyboard
import time
import networkx as nx
import matplotlib as plt
from math import dist

graph : list = load_graph_list(getGameData()["map_id"])
#graph = []

data = getGameData()
pos = (round(data['position'][0], 4), round(data['position'][1], 4))
old_pos = (round(data['position'][0], 4), round(data['position'][1], 4))

try:
    while True:
        if dist(pos, old_pos) > 0.6 and get_smallest_dist(graph, pos) > 0.6:
            if pos not in graph:
                graph.append(pos)
                old_pos = pos
                print(f"Added {pos} to graph")
            else:
                print("got it already")

        data = getGameData()
        pos = (round(data['position'][0], 4), round(data['position'][1], 4))

except KeyboardInterrupt:
    pass

write_graph_list(graph, data["map_id"])
 