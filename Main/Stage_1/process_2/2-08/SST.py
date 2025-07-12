import os
import csv
import sounddevice as sd
from scipy.io.wavfile import write
from datetime import datetime
import speech_recognition as sr

def record_voice(duration=5, samplerate=44100):
    print(" Start recording...")
    try:
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()
    except Exception as e:
        print(f"Failed to record: {e}")
        return None

    folder = "/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_1/process_2/2-7/records"
    os.makedirs(folder, exist_ok=True)

    now = datetime.now()
    filename = "record_" + now.strftime("%Y%m%d-%H%M%S") + ".wav"
    filepath = os.path.join(folder, filename)

    try:
        write(filepath, samplerate, recording)
        print(f"✅ Complete recording: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Failed to save file: {e}")
        return None

def list_wav_files(folder):
    return [f for f in os.listdir(folder) if f.lower().endswith('.wav')]

def speech_to_text(wav_path):
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)  # 전체 오디오 읽기
    try:
        text = r.recognize_google(audio, language='en-US')  # 영어 인식
        return text
    except sr.UnknownValueError:
        return "[인식 실패]"
    except sr.RequestError as e:
        return f"[API 오류: {e}]"

def save_text_to_csv(wav_path, text):
    csv_path = os.path.splitext(wav_path)[0] + ".csv"
    with open(csv_path, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Time(sec)", "Recognized Text"])
        # 전체 오디오를 한 덩어리로 인식했으므로 시간 0초에 전체 텍스트 저장
        writer.writerow([0, text])
    print(f"Saved STT result to {csv_path}")

def process_all_recordings():
    folder = "/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_1/process_2/2-07/records"
    wav_files = list_wav_files(folder)
    if not wav_files:
        print("녹음 파일이 없습니다.")
        return

    for wav_file in wav_files:
        wav_path = os.path.join(folder, wav_file)
        print(f"Processing {wav_path} ...")
        text = speech_to_text(wav_path)
        print(f"Recognized Text: {text}")
        save_text_to_csv(wav_path, text)

if __name__ == "__main__":
    # 1) 녹음
    # record_voice(duration=5)
    
    # 2) 녹음 폴더 내 모든 음성 파일 STT 처리 및 CSV 저장
    process_all_recordings()
