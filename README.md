# Behold: The Among Us AI!
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
0. Have python installed
1. Clone the repository and `pip install -r requirements.txt`
2. Copy `version.dll` and place it in your Among Us directory
3. Copy the path of your among us install folder and paste it in `sendDataDir.txt`
    - Right click the folder name "Among Us" from the top bar and select "Copy address as text"
4. Get an API key from your OpenAI account and paste it in a new file called `APIkey.txt`
    - https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key
    - you'll need to set up a payment method as their API is not free!
    - place the file in the same folder as `main.py`
5. Hop into a game and run `main.py`!
6. Press ` to stop the bot (you may need to press Ctrl+C in the command line to stop the script)

## Recommendations
- Install Among Us and this project on an SSD. The AI uses the disk to transfer data, so fast random read/write is important.
- 8GB DDR4 RAM (again for fast data transfer)
- Use Windows! The bot is untested on MacOS and Linux.
- The bot uses your mouse and keyboard. To forcibly stop it, press ctrl-alt-delete.

## Upcoming Features
- [ ] Support all maps (currently only Skeld is supported)
- [ ] Full voice chat support using OpenAI whisper
- [ ] Movement History
- [ ] Improved Imposter logic
- [ ] Venting

## Known Issues
- Optimizing route sometimes fails, so it walks further than normal
- Tasks that save your progress fail if partway done
- If a meeting is called as reactor/oxygen is happening, the AI will go there after the meeting
- Upload Data waits longer than it should. (Intentional: this prevents issues when the task lags)
- ChatGPT weirdness
