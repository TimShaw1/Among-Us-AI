from utility import get_task_list, load_dict
import subprocess

def generate_files():
    possible_tasks = load_dict().keys()
    for task in possible_tasks:
        with open(f"task-solvers\{task}.py", "w") as f:
            f.close()

tasks = get_task_list()[0]

def solve_task(task_name):
    return_code = subprocess.call(["python", f"task-solvers\{task_name}.py"])

solve_task("Align Engine Output")




