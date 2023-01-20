from utility import *
import keyboard
import time

graph = []

try:
    while True:
        data = getGameData()
        if data["position"][0] is None:
            continue
        pos = (round(data['position'][0], 4), round(data['position'][1], 4))
        if keyboard.is_pressed('i'):
            if pos not in graph:
                graph.append(pos)
                print("appended")
                time.sleep(0.1)
            else:
                print("got it already")
                time.sleep(0.1)

except KeyboardInterrupt:
    pass

print(points_to_gamepad(graph[0], graph[1]))
print(graph)

 