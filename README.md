# Behold: The Among Us AI!

![2024-06-15_10-18-54](https://github.com/TimShaw1/Among-Us-AI/assets/70497517/a7892d57-0d94-45da-b4a5-1658bd4647f1)

The Among Us AI is a bot that I designed in python to play the popular social deduction game Among Us. 

Here's a video I made detailing the creation process: https://youtu.be/VF41pxxw9uw

## Features
- Dynamic movement and intelligent task routing
- Automated task solving
- Full conversation capabilities powered by ChatGPT
- Intelligent sabotages and Kills
- Faking tasks
- and lots of gaslighting

## Setup Requirements
Video runthrough: https://youtu.be/N7ztLdSIjwQ

0. Have python installed (I used python 3.9.2)
1. Clone the repository and run the command `pip install -r requirements.txt`
2. Download the latest release from [releases](https://github.com/TimShaw1/Among-Us-AI/releases/latest) (both the source code zip AND AmongUsAI-BepInEx)
    - Extract the BepInEx zip file, then navigate in until you see the **BepInEx** folder (do **not** navigate into this folder)
    - Select every file, then drag and drop into your Among Us directory (Usually `C:\Program Files (x86)\Steam\steamapps\common\Among Us`)
    - Also extract the source code and open it in VS Code
3. Copy the path of your among us install folder and paste it in `sendDataDir.txt`
    - Right click the folder name "Among Us" from the top bar and select "Copy address as text"
4. Get an API key from your OpenAI account and paste it in a new file called `APIkey.txt`
    - https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key
    - you'll need to set up a payment method as their API is not free!
    - place the file in the same folder as `main.py`
5. Hop into a game (make sure game is windowed) and run `main.py`!
6. Press ` to stop the bot (you may need to press Ctrl+C in the command line to stop the script)

## Recommendations
- Install Among Us and this project on an SSD. The AI uses the disk to transfer data, so fast random read/write is important.
- 8GB DDR4 RAM (again for fast data transfer)
- Use Windows! The bot is untested on MacOS and Linux.
- The bot uses your mouse and keyboard. To stop it, hold ` for 7 seconds. To forcibly stop it, press ctrl-alt-delete.
- The game **must** be in windowed mode!

## Upcoming Features
- [ ] Support all maps (currently only Skeld and Polus are supported)
- [ ] Full voice chat support using OpenAI whisper
- [ ] Movement History
- [ ] Improved Imposter logic
- [ ] Venting

## Known Issues
- Optimizing route sometimes fails, so it walks further than normal
- ~Tasks that save your progress fail if partway done~
- If a meeting is called as reactor/oxygen is happening, the AI will go there after the meeting
- Upload Data waits longer than it should. (Intentional: this prevents issues when the task lags)
- ChatGPT weirdness
