import time
import os
import whisper

# ----------------------
# Load Whisper model
# ----------------------
model = whisper.load_model("base")   # or "tiny" if Pi struggles

# ----------------------
# System State
# ----------------------
MODE_NO_WORKOUT = 0
MODE_EXERCISE_SELECTED = 1
MODE_ACTIVE_WORKOUT = 2

current_mode = MODE_NO_WORKOUT
current_exercise = None

# ----------------------
# Command Actions
# ----------------------
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
    current_mode = MODE_EXERCISE_SELECTED
    print("[SYSTEM] Workout stopped.")

# ----------------------
# Command Recognition
# ----------------------
def process_transcription(text):
    text = text.lower()
    print(f"[DEBUG] Recognized text: {text}")

    detected = False

    if "start workout" or "workout started" in text:
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
        stop_workout()
        detected = True

    if not detected:
        print("[SYSTEM] No valid command recognized.")


# ----------------------
# Watch Folder
# ----------------------
WATCH_FOLDER = "./audio_commands"  # change this to your folder
processed_files = set()

def transcribe_file(path):
    print(f"[SYSTEM] Transcribing: {path}")
    result = model.transcribe(path)
    text = result["text"]
    process_transcription(text)

# ----------------------
# Main Loop
# ----------------------
print("[SYSTEM] Startup complete. No workout active.")
print("[SYSTEM] Waiting for audio files...\n")

while True:
    files = os.listdir(WATCH_FOLDER)

    for f in files:
        full_path = os.path.join(WATCH_FOLDER, f)

        # ignore already processed files
        if f not in processed_files and f.lower().endswith((".m4a", ".wav", ".mp3")):
            processed_files.add(f)
            transcribe_file(full_path)

    time.sleep(2)   # check every 2 seconds
