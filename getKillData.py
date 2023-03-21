import time
from utility import *

def save_kill_training_data():
    """
    Data must be of the form 
        {"nearby_players" : int, "nearby_imposters" : int, 
        
        "lights" : bool, "cams" : bool, 

        "current_area" : str, "num_players_alive" : int, 
        
        "num_imposters_alive" : int, "is_urgent" : bool}

    Saves the training example to kill-training-data\\example0.json
    """

    data = getGameData()

    # TODO: load_G is hardcoded to skeld
    G = load_G("SHIP")

    dict_to_send = {"nearby_players" : get_imposter_nearby_players(G), "nearby_imposters" : get_nearby_imposter_players(G), 
            "lights" : data["lights"], "cams" : are_cams_used(), "current_area" : data["room"], 
            "num_players_alive" : get_num_alive_players(), "num_imposters_alive" : get_num_alive_imposters(), 
            "is_urgent" : is_urgent_task() != None}
    
    example_num : int
    with open("kill-training-data\\Counter.txt", "r") as f:
        example_num = f.readline()
    f.close()

    with open("kill-training-data\\Counter.txt", "w") as f:
        f.write(f"{int(example_num) + 1}")
    f.close()

    with open(f"kill-training-data\\example{example_num}.json", "w") as f:
        json.dump(dict_to_send, f)
    f.close()

    if example_num % 100 == 0:
        output_str = ""
    elif example_num % 10 == 0:
        output_str = "0"
    else:
        output_str = "00"


    print(f"Saved kill example to kill-training-data\\example{output_str}{example_num}.json")

def main_loop():
    old_kill_timer = getImposterData()["killCD"]
    while isInGame():
        new_killCD = getImposterData()["killCD"]
        if new_killCD > old_kill_timer:
            save_kill_training_data()
            time.sleep(2)
            old_kill_timer = getImposterData()["killCD"]
        time.sleep(1/60)

while True:
    if not isInGame():
        time.sleep(1/30)
        continue
    if not isImpostor():
        time.sleep(5)
        continue
    main_loop()
    time.sleep(1)
