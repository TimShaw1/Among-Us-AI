import time
from utility import *
import win32gui, win32com.client
shell = win32com.client.Dispatch("WScript.Shell")

# DEPRECIATED

def save_kill_training_data(didKill : bool):
    """
    Data is of the form 
        {"nearby_players" : int, "nearby_imposters" : int, 
        
        "lights" : bool, "cams" : bool, 

        "num_players_alive" : int, 
        
        "num_imposters_alive" : int, "is_urgent" : bool
        
        "didKill" : bool}

    Saves the training example to kill-training-data\\example000.json
    """

    data = getGameData()

    G = load_G(data["map_id"])

    dict_to_send = {"nearby_players" : len(get_imposter_nearby_players(G)), "nearby_imposters" : len(get_nearby_imposter_players(G)), 
            "lights" : data["lights"], "cams" : are_cams_used(),  
            "num_players_alive" : get_num_alive_players(), "num_imposters_alive" : get_num_alive_imposters(), 
            "is_urgent" : is_urgent_task() != None, "didKill" : didKill}
    
    if (didKill):
        good = input("Was this a good kill? (y/n) ")
        if "n" in good:
            didKill = False
        shell.SendKeys(' ') #Undocks my focus from Python IDLE
        focus()
        shell.SendKeys('%')
    
    example_num : int
    with open(f"kill-training-data\\{int(didKill)}\\Counter.txt", "r") as f:
        example_num = f.readline()
    f.close()

    with open(f"kill-training-data\\{int(didKill)}\\Counter.txt", "w") as f:
        f.write(f"{int(example_num) + 1}")
    f.close()

    with open(f"kill-training-data\\{int(didKill)}\\example{example_num}.json", "w") as f:
        json.dump(dict_to_send, f)
    f.close()

    print(f"Saved kill example to kill-training-data\\{int(didKill)}\\example{example_num}.json")

def main_loop():
    """Unused file - could be used to collect training data for an imposter NN"""
    old_kill_timer = getImposterData()["killCD"]
    while isInGame():
        while in_meeting():
            time.sleep(10)
            old_kill_timer = getImposterData()["killCD"]
        while not can_kill():
            time.sleep(1/60)
            continue
        while can_kill():
            time.sleep(1/60)
            continue
        time.sleep(1/30)
        new_killCD = getImposterData()["killCD"]
        if new_killCD > old_kill_timer: # killed
            save_kill_training_data(True)
            time.sleep(5)
            old_kill_timer = getImposterData()["killCD"]
            continue
        else:
            save_kill_training_data(False)
            time.sleep(1)
            continue


while True:
    if not isInGame():
        time.sleep(1/30)
        continue
    if not isImpostor():
        time.sleep(5)
        continue
    main_loop()
    time.sleep(1)