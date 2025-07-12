import sounddevice as sd
from scipy.io.wavfile import write
import os
from datetime import datetime

def record_voice():
    try:
        duration = float(input("Enter recording duration (seconds): "))
    except ValueError:
        print("Invalid input. Using default duration 5 seconds.")
        duration = 5

    samplerate = 44100

    print(" Start recording...")
    try:
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()  # wait unt1il recording is done.
    except Exception as e:
        print(f"Failed to record: {e}")
        return

    folder = "/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_1/process_2/2-7/records"
    os.makedirs(folder, exist_ok=True)

    now = datetime.now()
    filename = "record_" + now.strftime("%Y%m%d-%H%M%S") + ".wav"
    filepath = os.path.join(folder, filename)

    try:
        write(filepath, samplerate, recording)
        print(f"✅ Complete recording: {filepath}")
    except Exception as e:
        print(f"❌ Failed to save file: {e}")

if __name__ == "__main__":
    record_voice()
