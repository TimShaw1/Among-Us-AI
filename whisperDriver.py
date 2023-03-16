import whisper
import time

t = time.time()


model = whisper.load_model("base.en")
result = model.transcribe("C:\\projects\\Whisper\\TestAudio\\AlpharadAudio.mp3")
print(result["text"])

print(f"Time:  {(time.time() - t)}")