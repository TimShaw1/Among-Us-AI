import utility
import subprocess
import time
import pyautogui
import random
import sys, os
import keyboard
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/task-solvers")
from task_utility import get_dimensions, get_screen_coords, wake

def generate_files():
    possible_tasks = utility.load_dict().keys()
    for task in possible_tasks:
        with open(f"task-solvers\{task}.py", "w") as f:
            f.close()

def chat(can_vote_flag : bool):
    if utility.isDead():
        while utility.in_meeting():
            time.sleep(1/60)
            continue
        return
    p = subprocess.Popen(["python", f"chatGPT.py"])
    while p.poll() is None:
        if keyboard.is_pressed('`'):
            p.kill()
            utility.clear_kill_data()
            return
    p.wait()
    while utility.in_meeting():
        time.sleep(1/60)
    p.kill()
    utility.clear_kill_data()

def solve_task(task_name=None, task_location=None) -> int:
    """ 
    Runs the correct task solver file in a subprocess

    Note - the AI only goes to the upper location of sabotages

    Returns
    --------
    int
        0 if success

        1 if meeting was called or died

        2 if a meeting was called and the task was inspect sample (so it doesn't wait later)
        
        -1 if task not found
    """
    dead : bool = utility.isDead()
    if task_name == "vote":
        print("Should never be here")
        if not dead:
            p = subprocess.Popen(["python", f"task-solvers\\vote.py"])
        else:
            return 0
        p.wait()
        return 0

    if utility.isImpostor():
        # Record last task done
        if not utility.isDead():
            with open("last_task.txt", "w") as f:
                f.write(f"{task_name} in {task_location}")
            f.close()
        time.sleep(1.5)
        urgent = utility.is_urgent_task()
        if urgent is None:
            # Open solver file
            if random.randint(1,3) % 3 == 0:
                p = subprocess.Popen(["python", f"task-solvers\Sabotage.py"])
            else:
                return 0
        else:
            if utility.in_meeting():
                return 1
            return 0

        # Wait for process to finish
        while p.poll() is None:
            if utility.in_meeting() or keyboard.is_pressed('`'):
                p.kill()
                return 1
            time.sleep(1/30)

        time.sleep(3) # Fake doing stuff
        return 0
    
    if utility.is_urgent_task() is not None:
        if task_name is not None and task_name != utility.is_urgent_task()[0]:
            return 1

    if task_name is not None and task_name != ():
        # Record last task done
        with open("last_task.txt", "w") as f:
            f.write(f"{task_name} in {task_location}")
        f.close()

        # Open solver file
        p = subprocess.Popen(["python", f"task-solvers\{task_name}.py"])

        # Wait for process to finish
        while p.poll() is None:
            if utility.in_meeting() or (utility.isDead() != dead) or keyboard.is_pressed('`'):
                p.kill()
                return 1 if task_name != "Inspect Sample" else 2
            time.sleep(1/30)

        return 2 if task_name == "Inspect Sample" else 0
    
    print("Task not found")
    return -1

