import sys
import os
import csv
import sounddevice as sd
from scipy.io.wavfile import write, read
from datetime import datetime
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox, QComboBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt

# 녹음 파일 및 메타데이터를 저장할 기본 경로
RECORDS_FOLDER = "/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_1/process_2/2-07/records"

class STTProcessor(QThread):
    """
    음성 파일을 텍스트로 변환하는 STT (Speech to Text) 기능을 수행하는 스레드 클래스입니다.
    """
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        """
        별도 스레드에서 음성 파일을 텍스트로 변환하고 결과를 CSV로 저장합니다.
        """
        recognizer = sr.Recognizer()
        print(f"Processing {self.file_path} for STT...")

        try:
            # SciPy로 WAV 파일 로드
            samplerate, audio_data = read(self.file_path)
            
            # SpeechRecognition의 AudioData 형식으로 변환
            audio = sr.AudioData(audio_data.tobytes(), samplerate, 2) # 2 bytes per sample for 16-bit

            # 구글 웹 음성 API를 사용하여 음성 인식
            text = recognizer.recognize_google(audio, language='ko-KR')
            print(f"Recognized Text: {text}")

            self.save_text_to_csv(text)
            self.finished.emit(self.file_path)
            
        except sr.UnknownValueError:
            error_msg = f"Speech Recognition could not understand audio in {os.path.basename(self.file_path)}"
            self.error.emit(error_msg)
            self.save_text_to_csv("[인식 실패]")
        except sr.RequestError as e:
            error_msg = f"Could not request results from Google Speech Recognition service; {e}"
            self.error.emit(error_msg)
            self.save_text_to_csv(f"[API 오류: {e}]")
        except Exception as e:
            error_msg = f"An unexpected error occurred during STT: {e}"
            self.error.emit(error_msg)
            self.save_text_to_csv(f"[알 수 없는 오류: {e}]")

    def save_text_to_csv(self, text):
        """
        인식된 텍스트를 CSV 파일로 저장합니다.
        """
        # WAV 파일명과 동일한 CSV 파일명 생성
        csv_path = os.path.splitext(self.file_path)[0] + ".csv"
        with open(csv_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Time(sec)", "Recognized Text"])
            writer.writerow([0, text])
        print(f"Saved STT result to {csv_path}")


class VoiceRecorder(QThread):
    """
    마이크를 사용하여 음성을 녹음하고 파일로 저장하는 클래스입니다.
    """
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, duration=5, samplerate=44100, device_index=None):
        super().__init__()
        self.duration = duration
        self.samplerate = samplerate
        self.device_index = device_index

    def run(self):
        print("Start recording...")
        try:
            recording = sd.rec(
                int(self.duration * self.samplerate), 
                samplerate=self.samplerate, 
                channels=1, 
                dtype='int16',
                device=self.device_index
            )
            sd.wait()
            
            os.makedirs(RECORDS_FOLDER, exist_ok=True)

            now = datetime.now()
            filename_base = now.strftime("%Y%m%d-%H%M%S")
            filepath_wav = os.path.join(RECORDS_FOLDER, f"{filename_base}.wav")
            
            write(filepath_wav, self.samplerate, recording)
            print(f"✅ Complete recording: {filepath_wav}")
            
            # 녹음 직후 STT 처리
            stt_thread = STTProcessor(filepath_wav)
            stt_thread.finished.connect(lambda: self.finished.emit(filepath_wav))
            stt_thread.error.connect(self.error.emit)
            stt_thread.start()

        except Exception as e:
            print(f"❌ Failed to record or save file: {e}")
            self.error.emit(str(e))
            
class JavisApp(QWidget):
    """
    음성 녹음 및 STT 기능을 위한 UI를 제공하는 애플리케이션 클래스입니다.
    """
    def __init__(self):
        super().__init__()
        self.recorder = None
        self.initUI()
        self.initDevices()
        self.initProcessExistingFilesButton()

    def initUI(self):
        self.setWindowTitle("Javis Voice Recorder & STT")
        self.setFixedSize(400, 250)

        self.status_label = QLabel("Ready to record.")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        self.record_button = QPushButton("Start Recording (5s)")
        self.record_button.clicked.connect(self.start_recording)

        self.process_files_button = QPushButton("Process Existing Files (STT)")
        self.process_files_button.clicked.connect(self.process_all_recordings)

        self.device_combo = QComboBox()

        vbox = QVBoxLayout()
        vbox.addWidget(self.status_label)
        vbox.addWidget(QLabel("Select Microphone:"))
        vbox.addWidget(self.device_combo)
        vbox.addWidget(self.record_button)
        vbox.addWidget(self.process_files_button)

        self.setLayout(vbox)

    def initDevices(self):
        try:
            devices = sd.query_devices()
            input_devices = [d for d in devices if d['max_input_channels'] > 0]
            if not input_devices:
                self.status_label.setText("No input devices found!")
                self.record_button.setEnabled(False)
                return

            for i, device in enumerate(input_devices):
                self.device_combo.addItem(f"{device['name']} (idx: {device['index']})", device['index'])

        except Exception as e:
            self.status_label.setText("Error fetching devices.")
            QMessageBox.critical(self, "Device Error", f"Failed to get audio devices:\n{e}")
            self.record_button.setEnabled(False)
    
    def initProcessExistingFilesButton(self):
        if not os.path.exists(RECORDS_FOLDER) or not any(f.endswith('.wav') for f in os.listdir(RECORDS_FOLDER)):
            self.process_files_button.setEnabled(False)

    def start_recording(self):
        device_index = self.device_combo.currentData()
        if device_index is None:
            QMessageBox.warning(self, "No Device Selected", "Please select a microphone.")
            return

        self.recorder = VoiceRecorder(device_index=device_index)
        self.recorder.finished.connect(self.on_recording_finished)
        self.recorder.error.connect(self.on_recording_error)

        self.status_label.setText("Recording...")
        self.record_button.setEnabled(False)
        self.process_files_button.setEnabled(False)
        self.recorder.start()

    def process_all_recordings(self):
        self.status_label.setText("Processing existing files...")
        self.record_button.setEnabled(False)
        self.process_files_button.setEnabled(False)
        
        wav_files = [f for f in os.listdir(RECORDS_FOLDER) if f.lower().endswith('.wav')]
        if not wav_files:
            QMessageBox.information(self, "No Files", "No WAV files found in the records folder.")
            self.on_stt_finished()
            return
        
        for wav_file in wav_files:
            wav_path = os.path.join(RECORDS_FOLDER, wav_file)
            stt_thread = STTProcessor(wav_path)
            stt_thread.finished.connect(lambda: self.on_stt_finished())
            stt_thread.error.connect(self.on_stt_error)
            stt_thread.start()

    def on_stt_finished(self):
        self.status_label.setText("STT processing complete.")
        self.record_button.setEnabled(True)
        self.process_files_button.setEnabled(True)
        QMessageBox.information(self, "STT Complete", "All existing WAV files have been processed.")
        
    def on_stt_error(self, message):
        self.status_label.setText("STT processing error.")
        self.record_button.setEnabled(True)
        self.process_files_button.setEnabled(True)
        QMessageBox.critical(self, "STT Error", f"An error occurred during STT:\n{message}")

    def on_recording_finished(self, filepath):
        self.status_label.setText("Recording complete. Starting STT...")
        # STT는 VoiceRecorder 스레드 내부에서 자동으로 시작됩니다.
        # on_stt_finished/on_stt_error가 호출되면 버튼이 활성화됩니다.

    def on_recording_error(self, message):
        self.status_label.setText("Recording failed.")
        self.record_button.setEnabled(True)
        self.process_files_button.setEnabled(True)
        QMessageBox.critical(self, "Recording Error", f"An error occurred during recording:\n{message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = JavisApp()
    ex.show()
    sys.exit(app.exec_())