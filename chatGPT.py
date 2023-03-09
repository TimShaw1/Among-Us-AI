import openai
from utility import getGameData, in_meeting

API_KEY = "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"

data = getGameData()
while not data['tasks']:
    data = getGameData()

openai.api_key = API_KEY
color : str = data['color']
role : str = "impostor" #data['status']
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
                 f'''You are playing the game Among Us and have been called sus. You are in a meeting with your crewmate. 
                 The prompts you see are messages from your crewmates. You are {color}. Your role is {role}. Your tasks are {tasks}.
                 Your tasks are in {task_locations}.
                 You can choose not to respond if you have nothing to add by saying "None". Reply to prompts with very few words and don't be too formal.
                 Try to win by voting the impostor out. If your role is impostor, try to get other people voted off by calling them sus and suggesting the group vote them off.'''
                 }
            ]

# TODO: While in_meeting()
while True:
    prompt = input("Ask me something: ")
    if prompt == "exit":
        break
    
    prompts.append({"role": "user", "content": prompt})
    response = ask_gpt(prompts)
    prompts.append({"role": "assistant", "content": response})
    print(response)