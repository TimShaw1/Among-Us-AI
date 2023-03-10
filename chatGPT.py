import openai
from utility import getGameData, in_meeting, get_chat_messages, clear_chat
import time

API_KEY = "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"

data = getGameData()

openai.api_key = API_KEY
color : str = data['color']
role : str = data['status']
tasks : str = ' '.join(data['tasks'])
task_locations : str = ' '.join(data['task_locations'])

print(tasks)
print(task_locations)
print()

def ask_gpt(prompts : str) -> str: 
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompts
    )

    message = response['choices'][0]['message']['content']
    return message.rstrip()

prompts =   [
                {"role": "system", "content": 
                 f'''You are playing the game Among Us. You are in a meeting with your crewmates. 
                 The prompts you see are messages from your crewmates. You are {color}. Your role is {role}. Your tasks are {tasks}.
                 Your tasks are in {task_locations}. Your crewmates' and your messages are identified by their color in the prompt. You can only reply as your color.
                 You can choose not to respond if you have nothing to add by saying "None". Reply to prompts with very few words and don't be too formal.
                 Try to win by voting the impostor out. If your role is impostor, try to get other people voted off by calling them sus and suggesting the group vote them off.'''
                 }
            ]

clear_chat()
seen_chats = []
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
            response = ask_gpt(prompts)
            print(response)
            time.sleep(5)
    except openai.error.RateLimitError:
        print("Rate limit reached")
        break