import time
from utility import *


def printConstantGameData():
    try:
        while True:
            data = getGameData()
            if not data:
                continue
            for key in data.keys():
                print(data[key])
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


if __name__ == "__main__":
    printGameData()


