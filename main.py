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
    while not data:
        data = getGameData()
    for key in data.keys():
        print(data[key])
    print()


if __name__ == "__main__":
    printConstantGameData()


