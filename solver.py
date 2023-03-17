from utility import get_task_list, load_dict, in_meeting, isImpostor, is_urgent_task, isDead, can_vote, clear_kill_data
import subprocess
import time
import pyautogui
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/task-solvers")
from task_utility import get_dimensions, get_screen_coords, wake

def generate_files():
    possible_tasks = load_dict().keys()
    for task in possible_tasks:
        with open(f"task-solvers\{task}.py", "w") as f:
            f.close()

def chat(can_vote_flag : bool):
    if isDead():
        while in_meeting():
            time.sleep(1/60)
            continue
        return
    p = subprocess.Popen(["python", f"chatGPT.py"])
    p.wait()
    while in_meeting():
        time.sleep(1/60)
    p.kill()
    clear_kill_data()

# Runs the correct task solver file in a subprocess
# Note - the AI only goes to the upper location of sabotages
def solve_task(task_name=None, task_location=None) -> int:
    dead : bool = isDead()
    if task_name == "vote":
        print("Should never be here")
        if not dead:
            p = subprocess.Popen(["python", f"task-solvers\\vote.py"])
        else:
            return 0
        p.wait()
        return 0

    if isImpostor():
        with open("last_task.txt", "w") as f:
            f.write(f"{task_name} in {task_location}")
        f.close()
        time.sleep(1.5)
        urgent = is_urgent_task()
        if urgent is None:
            p = subprocess.Popen(["python", f"task-solvers\Sabotage.py"])
        else:
            if in_meeting():
                return 1
            return 0

        # Wait for process to finish
        while p.poll() is None:
            if in_meeting():
                p.kill()
                return 1
            time.sleep(1/30)

        time.sleep(3) # Fake doing stuff
        return 0
    
    if is_urgent_task() is not None:
        if task_name is not None and task_name != is_urgent_task()[0]:
            return 1

    if task_name is not None and task_name != ():
        with open("last_task.txt", "w") as f:
            f.write(f"{task_name} in {task_location}")
        f.close()
        p = subprocess.Popen(["python", f"task-solvers\{task_name}.py"])

        # Wait for process to finish
        while p.poll() is None:
            if in_meeting() or (isDead() != dead):
                p.kill()
                return 1 if task_name != "Inspect Sample" else 2
            time.sleep(1/30)

        return 0
    
    print("Task not found")
    return -1

