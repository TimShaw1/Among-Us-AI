import openai
from utility import getGameData, in_meeting, get_chat_messages, clear_chat
import time
import pyautogui
import re
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/task-solvers")
from task_utility import get_dimensions, get_screen_coords

API_KEY = "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"

data = getGameData()

openai.api_key = API_KEY
color : str = data['color']
role : str = data['status']
tasks : str = ' '.join(data['tasks'])
task_locations : str = ' '.join(data['task_locations'])

def ask_gpt(prompts : str) -> str: 
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompts
    )

    message = response['choices'][0]['message']['content']
    return message.rstrip()

prompts =   [
                {"role": "user", "content": 
                 re.sub(' +', ' ', f'''You are playing the game Among Us. You are in a meeting with your crewmates. 
                 The prompts you see that are not from you, {color}, are messages from your crewmates. You are {color}. Your role is {role}. Your tasks are {tasks}.
                 Your tasks are in {task_locations}. Your crewmates' and your messages are identified by their color in the prompt. 
                 You can only reply as your color. You should only return text that your player, {color}, is saying. Do not return text in the form (COLOR that isn't {color}): (response)
                 Reply to prompts with very few words and don't be too formal. 
                 Reply with at most 1 to 2 sentences. Never return more than 100 words at a time.
                 Try to win by voting the impostor out. If your role is impostor, try to get other people voted off by calling them sus and suggesting the group vote them off.
                 Only return messages from the {color} player.'''.replace('\n', ' '))
                 },

                 {"role": "assistant", "content": "GRAY: anyone sus?"},
                 {"role": "user", "content": "BLUE: Idk"},
                 {"role": "assistant", "content": "GRAY: okay"}
            ]

dimensions = get_dimensions()

x = dimensions[0] + round(dimensions[2] / 1.27)
y = dimensions[1] + round(dimensions[3] / 7.77)
pyautogui.click(x,y)
time.sleep(0.5)

x = dimensions[0] + round(dimensions[2] / 4.54)
y = dimensions[1] + round(dimensions[3] / 1.19)

pyautogui.typewrite("Anyone sus?\n")
clear_chat()
seen_chats = []
pyautogui.click(x,y)
time.sleep(0.1)
time.sleep(5)
# TODO: While in_meeting()
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
            print(response)
            pyautogui.typewrite(f"{response}\n")
            time.sleep(5)
    except openai.error.RateLimitError:
        print("Rate limit reached")
        break