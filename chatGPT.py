import openai
from utility import getGameData, in_meeting, get_chat_messages, clear_chat, translatePlayerColorID, allTasksDone, get_nearby_players, load_G
import time
import pyautogui
import networkx as nx
import re
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/task-solvers")
from task_utility import get_dimensions, get_screen_coords, wake

with open("APIkey.txt") as f:
    API_KEY = f.readline().rstrip()


data = getGameData()

openai.api_key = API_KEY
color : str = data['color']
role : str = data['status']
tasks : str = ' '.join(data['tasks'])
task_locations : str = ' '.join(data['task_locations'])
G = load_G("SHIP")
print(G)
nearby_players = get_nearby_players(G)

def get_caller_color():
    with open("sendDataDir.txt") as f:
        line = f.readline().rstrip()
        MEETING_PATH = line + "\\meetingData.txt"
    f.close()
    with open(MEETING_PATH) as f:
        line = f.readline().rstrip()
        return translatePlayerColorID(int(line))
    
def get_dead_players():
    with open("sendDataDir.txt") as f:
        line = f.readline().rstrip()
        MEETING_PATH = line + "\\meetingData.txt"
    f.close()
    with open(MEETING_PATH) as f:
        f.readline().rstrip()
        line = f.readline().rstrip()
        return [translatePlayerColorID(int(x)) for x in line.strip('][').split(", ")[:-1]]
    
def get_last_task():
    with open("last_task.txt") as f:
        line = f.readline().rstrip()
        return line
    
def get_last_room():
    with open("last_area.txt") as f:
        line = f.readline().rstrip()
        return line

def ask_gpt(prompts : str) -> str: 
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompts
    )

    message = response['choices'][0]['message']['content']
    return message.rstrip()

tasks_prompt = "You finished all your tasks" if allTasksDone() else f"Your last completed task was {get_last_task()}"

# Before the meeting, you were {"not near anyone" if len(nearby_players) == 0 else "near " + nearby_players}
prompts =   [
                {"role": "system", "content": 
                 re.sub(' +', ' ', f'''You are playing the game Among Us. You are in a meeting with your crewmates. 
                 {get_caller_color()} called the meeting. {str(get_dead_players()).strip("][").replace("'", '')} are dead. {tasks_prompt}. The last room you were in was {get_last_room()}.
                 The prompts you see that are not from you, {color}, are messages from your crewmates. You are {color}. Your role is {role}. Your tasks are {tasks}.
                 Your name is Duper. People can refer to you by your name or your color. Your tasks are in {task_locations}. Your crewmates' and your messages are identified by their color in the prompt. 
                 Reply to prompts with very few words and don't be formal. Try to only use 1 sentence, preferably an improper one. Never return more than 100 words at a time.
                 Try to win by voting the impostor out. If your role is impostor, try to get other people voted off by calling them sus and suggesting the group vote them off.
                 Only return messages from the {color} player.'''.replace('\n', ' '))
                 },

                 {"role": "system", "content": "If someone says 'where' without much context, they are asking where the body was found"},
                 {"role": "system", "content": f"If someone says 'what' or '?' without much context, they are asking {get_caller_color()} why the meeting was called"}
            ]

clear_chat()
seen_chats = []
time.sleep(5)

dimensions = get_dimensions()

x = dimensions[0] + round(dimensions[2] / 1.27)
y = dimensions[1] + round(dimensions[3] / 7.77)
wake()
pyautogui.click(x,y, duration=0.2)
time.sleep(0.5)

x = dimensions[0] + round(dimensions[2] / 4.54)
y = dimensions[1] + round(dimensions[3] / 1.19)

pyautogui.click(x,y)
time.sleep(0.1)
time.sleep(5)

while True:
    new_chats = False
    chat_history = get_chat_messages()
    
    for chat in chat_history:
        if chat not in seen_chats:
            if f"{color}: " in chat:
                prompts.append({"role": "assistant", "content": chat})
            else:
                prompts.append({"role": "user", "content": chat})
            seen_chats.append(chat)
            new_chats = True

    try:
        if new_chats:
            pyautogui.click(x,y)
            time.sleep(0.1)
            response = ask_gpt(prompts)
            new_response = " "
            for line in response.splitlines():
                if f"{color}: " not in line:
                    print("skipped")
                    continue
                new_response += line

            response = new_response.replace(f'{color}: ', '')
            print("res: " + response)
            pyautogui.typewrite(f"{response.lower()}\n")
            time.sleep(5)
    except openai.error.RateLimitError:
        print("Rate limit reached")
        break