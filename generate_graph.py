from utility import *
import keyboard
import time
import networkx as nx
import matplotlib as plt
from math import dist

graph = get_graph_list("SHIP")

data = getGameData()
while not data['position'][0]:
    data = getGameData()
pos = (round(data['position'][0], 4), round(data['position'][1], 4))
old_pos = (round(data['position'][0], 4), round(data['position'][1], 4))

try:
    while True:
        if dist(pos, old_pos) > 0.7 and get_smallest_dist(graph, pos) > 0.7:
            if pos not in graph:
                graph.append(pos)
                old_pos = pos
                print("appended")
            else:
                print("got it already")

        data = getGameData()
        while not data['position'][0]:
            data = getGameData()
        pos = (round(data['position'][0], 4), round(data['position'][1], 4))

except KeyboardInterrupt:
    pass

#print(graph)
print(len(graph))
#write_graph_list(graph, "SHIP")
 