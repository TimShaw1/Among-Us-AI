from utility import get_task_list, load_dict
import subprocess

def generate_files():
    possible_tasks = load_dict().keys()
    for task in possible_tasks:
        with open(f"task-solvers\{task}.py", "w") as f:
            f.close()

def solve_task(task_name=None, task_index=None):
    tasks = get_task_list()[0]
    if task_name is not None:
        print(task_name)
        return_code = subprocess.call(["python", f"task-solvers\{task_name}.py"])
        return return_code
    if task_index is not None:
        return_code = subprocess.call(["python", f"task-solvers\{tasks[task_index]}.py"])
        return return_code
    print("error")

if __name__ == "__main__":
    solve_task("Align Engine Output")




