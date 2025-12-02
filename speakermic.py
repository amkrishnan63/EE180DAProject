import time
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write as wav_write
from faster_whisper import WhisperModel


model = WhisperModel("base", device="cpu")


MODE_NO_WORKOUT = 0
MODE_EXERCISE_SELECTED = 1
MODE_ACTIVE_WORKOUT = 2

current_mode = MODE_NO_WORKOUT
current_exercise = None


def set_exercise(ex):
    global current_mode, current_exercise
    current_exercise = ex
    current_mode = MODE_EXERCISE_SELECTED
    print(f"[SYSTEM] Exercise set to {ex}")

def start_workout():
    global current_mode
    current_mode = MODE_ACTIVE_WORKOUT
    print("[SYSTEM] Workout started.")

def stop_workout():
    global current_mode
    current_mode = MODE_NO_WORKOUT
    print("[SYSTEM] Workout stopped.")
    print("[SYSTEM] System shutting down...")   
    raise SystemExit                        
def process_transcription(text):
    text = text.lower().strip()
    print(f"[DEBUG] Recognized text: {text}")

    detected = False

    if "start workout" in text or "workout started" in text:
        start_workout()
        detected = True

    if "switch to squat" in text:
        set_exercise("squat")
        detected = True

    if "switch to deadlift" in text:
        set_exercise("deadlift")
        detected = True

    if "switch to bench press" in text or "switch to bench" in text:
        set_exercise("bench press")
        detected = True

    if "stop workout" in text or "workout stopped" in text:
        stop_workout()     # <<< This will terminate the program
        detected = True

    if not detected:
        print("[SYSTEM] No valid command recognized.")



def listen_and_transcribe(duration=5, sample_rate=16000):
    print("\n[SYSTEM] Listening...")

    audio = sd.rec(int(duration * sample_rate),
                   samplerate=sample_rate,
                   channels=1,
                   dtype="float32")
    sd.wait()

    audio_int16 = np.int16(audio * 32767)
    temp_file = "temp_audio.wav"
    wav_write(temp_file, sample_rate, audio_int16)

    segments, info = model.transcribe(temp_file, language="en")
    text = " ".join([seg.text for seg in segments]).strip()

    return text


print("[SYSTEM] Live voice control active!")
print("[SYSTEM] Speak any command: start workout, stop workout, switch to squat...\n")

while True:
    text = listen_and_transcribe()

    if text:
        process_transcription(text)

    time.sleep(0.2)

