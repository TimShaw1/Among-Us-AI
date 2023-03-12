import openai
from utility import getGameData, in_meeting, get_chat_messages, clear_chat
import time
import pyautogui
import re
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/task-solvers")
from task_utility import get_dimensions, get_screen_coords, wake

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
                {"role": "system", "content": 
                 re.sub(' +', ' ', f'''You are playing the game Among Us. You are in a meeting with your crewmates. 
                 The prompts you see that are not from you, {color}, are messages from your crewmates. You are {color}. Your role is {role}. Your tasks are {tasks}.
                 Your name is Duper. People can refer to you by your name or your color. Your tasks are in {task_locations}. Your crewmates' and your messages are identified by their color in the prompt. 
                 Reply to prompts with very few words and don't be formal. Try to only use 1 sentence, preferably an improper one. Never return more than 100 words at a time.
                 Try to win by voting the impostor out. If your role is impostor, try to get other people voted off by calling them sus and suggesting the group vote them off.
                 Only return messages from the {color} player.'''.replace('\n', ' '))
                 },

                 {"role": "system", "content": "If someone says 'where' without much context, they are asking where the body was found"}
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