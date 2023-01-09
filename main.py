import time

SHIP_TASK_TYPES = {
                    "Align Engine Output" : {"Upper Engine" : (-19.0939, -1.25595), "Lower Engine": (-18.9193, -13.4284)}, "Calibrate Distributor" : {"Electrical" : (-5.9473, -8.26674)}, "Chart Course" : {}, "Clean O2 Filter" : {"Oxygen" : (5.875643, -3.462795)}, "Vent Cleaning" : {}, 
                    "Clear Asteroids" : {}, "Divert Power" : {"Electrical" : (-8.96235, -8.07017), "Oxygen" : (8.30059, -3.15958)}, "Empty Chute" : {}, "Empty Garbage" : {}, 
                    "Fix Wiring" : {"Electrical" : (-7.7823, -8.10193), "Storage" : (-1.8403, -9.40424), "Cafeteria" : (-5.12926, 4.7277)}, "Fuel Engines" : {}, "Inspect Sample" : {}, 
                    "Prime Shields" : {}, "Stabilize Steering" : {}, "Start Reactor" : {}, "Submit Scan" : {}, "Swipe Card" : {}, "Unlock Manifolds" : {}, "Upload Data" : {}
                  }

AIRSHIP_TASK_TYPES = {  
                        "Calibrate Distributor" : {}, "Clean Toilet" : {}, "Vent Cleaning" : {}, "Decontaminate" : {}, "Develop Photos" : {}, "Divert Power" : {}, 
                        "Dress Mannequin" : {}, "Empty Garbage" : {}, "Enter ID Code" : {}, "Fix Shower" : {}, "Fix Wiring" : {}, "Fuel Engines" : {}, "Make Burger" : {}, 
                        "Pick Up Towels" : {}, "Polish Ruby" : {}, "Put Away Pistols" : {}, "Put Away Rifles" : {}, "Reset Breakers" : {}, "Rewind Tapes" : {}, 
                        "Sort Records" : {}, "Stabilize Steering" : {}, "Start Fans" : {}, "Unlock Safe" : {}, "Upload Data" : {}
                     }

PB_TASK_TYPES = {   
                    "Align Telecopse" : {}, "Chart Course" : {}, "Clear Asteroids" : {}, "Empty Garbage" : {}, "Fill Canisters" : {}, "Activate Weather Nodes" : {}, 
                    "Fix Wiring" : {}, "Fuel Engines" : {}, "Insert Keys" : {}, "Inspect Sample" : {}, "Monitor Oxygen" : {}, "Open Waterways" : {}, "Reboot Wifi" : {}, 
                    "Record Temperature" : {}, "Repair Drill" : {}, "Replace Water Jug" : {}, "Scan Boarding Pass" : {}, "Start Reactor" : {}, "Store Artifacts" : {}, 
                    "Submit Scan" : {}, "Swipe Card" : {}, "Unlock Manifolds" : {}, "Upload Data" : {}
                }

HQ_TASK_TYPES = {   
                    "Assemble Artifact" : {}, "Buy Beverage" : {}, "Chart Course" : {}, "Clean O2 Filter" : {}, "Vent Cleaning" : {}, "Clear Asteroids" : {}, 
                    "Divert Power" : {}, "Empty Garbage" : {}, "Enter ID Code" : {}, "Fix Wiring" : {}, "Fuel Engines" : {}, "Measure Weather" : {}, "Prime Shields" : {}, 
                    "Process Data" : {}, "Run Diagnostics" : {}, "Sort Samples" : {}, "Start Reactor" : {}, "Submit Scan" : {}, "Unlock Manifolds" : {}, "Water Plants" : {}
                }

UNUSED_TASKS = ["Reset Reactor", "Fix Lights", "Fix Communications", "Restore Oxygen", "Reset Seismic Stabilizers", "Get Biggol Sword", "Stop Charles"]

SEND_DATA_PATH = "sendData.txt"

def getGameData():
    x,y,status,tasks, task_locations, map_id = None, None, None, None, None, None
    with open(SEND_DATA_PATH) as file:
        lines = file.readlines()
        if len(lines) > 0:
            x = float(lines[0].split()[0])
            y = float(lines[0].split()[1])
            status = lines[1].strip()
            if len(lines) > 2:
                tasks = lines[2].rstrip().strip('][').split(", ")
            if len(lines) > 3:
                task_locations = lines[3].rstrip().strip('][').split(", ")
            if len(lines) > 4:
                map_id = lines[4].rstrip()

    return {"position" : (x,y), "status" : status, "tasks" : tasks, "task_locations" : task_locations, "map_id" : map_id}

def printConstantGameData():
    try:
        while True:
            data = getGameData()
            if not data:
                continue
            print(data["position"])
            print(data["status"])
            print(data["tasks"])
            print(data["task_locations"])
            print(data["map_id"])
            print()
            time.sleep(2)

    except KeyboardInterrupt:
        pass

def printGameData():
    data = getGameData()
    while not data:
        data = getGameData()
    print(data["position"])
    print(data["status"])
    print(data["tasks"])
    print(data["task_locations"])
    print(data["map_id"])
    print()

if __name__ == "__main__":
    printGameData()
    data = getGameData()


