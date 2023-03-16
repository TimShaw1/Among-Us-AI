import whisper
import time

t = time.time()


model = whisper.load_model("small.en")
result = model.transcribe("C:\\projects\\Whisper\\TestAudio\\test2.wav")
print(result["text"])
result = model.transcribe("C:\\projects\\Whisper\\TestAudio\\AlpharadAudio.mp3")
print(result["text"])

print(f"Time:  {(time.time() - t)}")