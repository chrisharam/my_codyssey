import sys
import sounddevice as sd
from scipy.io.wavfile import write
import os
from datetime import datetime
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox, QComboBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt

# 녹음 파일 및 메타데이터를 저장할 기본 경로
RECORDS_FOLDER = "/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_1/process_2/2-07/records"

class VoiceRecorder(QThread):
    """
    마이크를 사용하여 음성을 녹음하고 파일로 저장하는 클래스입니다.
    QThread를 상속하여 UI가 멈추지 않고 백그라운드에서 녹음 작업을 수행합니다.
    """
    finished = pyqtSignal(str)  # 녹음 완료 신호, 파일 경로를 전달
    error = pyqtSignal(str)     # 오류 발생 신호, 오류 메시지를 전달

    def __init__(self, duration=5, samplerate=44100, device_index=None):
        super().__init__()
        self.duration = duration
        self.samplerate = samplerate
        self.device_index = device_index

    def run(self):
        """
        별도 스레드에서 녹음을 시작하고 파일을 저장합니다.
        """
        print("Start recording...")
        try:
            # 녹음 장치 인덱스를 사용하여 녹음 시작
            recording = sd.rec(
                int(self.duration * self.samplerate), 
                samplerate=self.samplerate, 
                channels=1, 
                dtype='int16',
                device=self.device_index
            )
            sd.wait()  # 녹음이 끝날 때까지 대기
            
            # 레코드 폴더가 없으면 생성
            os.makedirs(RECORDS_FOLDER, exist_ok=True)

            # '년월일-시분초.wav' 형식의 파일명 생성
            now = datetime.now()
            filename_base = now.strftime("%Y%m%d-%H%M%S")
            filepath_wav = os.path.join(RECORDS_FOLDER, f"{filename_base}.wav")
            filepath_csv = os.path.join(RECORDS_FOLDER, f"{filename_base}.csv")

            # WAV 파일로 저장
            write(filepath_wav, self.samplerate, recording)
            print(f"✅ Complete recording: {filepath_wav}")

            # CSV 파일에 메타데이터 저장
            with open(filepath_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Time(sec)', 'Recognized Text'])
                
                # 예시 데이터 (음성 인식 기능이 없으므로 고정값 사용)
                writer.writerow(['0', 'stuff'])
            print(f"✅ Complete metadata: {filepath_csv}")
            
            self.finished.emit(filepath_wav)  # UI에 완료 신호 전송

        except Exception as e:
            print(f"❌ Failed to record or save file: {e}")
            self.error.emit(str(e))  # UI에 오류 신호 전송
            
class JavisApp(QWidget):
    """
    음성 녹음 기능을 위한 간단한 UI를 제공하는 애플리케이션 클래스입니다.
    """
    def __init__(self):
        super().__init__()
        self.recorder = None
        self.initUI()
        self.initDevices()

    def initUI(self):
        """UI 구성 요소를 설정합니다."""
        self.setWindowTitle("Javis Voice Recorder")
        self.setFixedSize(300, 200)

        self.status_label = QLabel("Ready to record.")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        self.record_button = QPushButton("Start Recording (5s)")
        self.record_button.clicked.connect(self.start_recording)

        self.device_combo = QComboBox()

        vbox = QVBoxLayout()
        vbox.addWidget(self.status_label)
        vbox.addWidget(QLabel("Select Microphone:"))
        vbox.addWidget(self.device_combo)
        vbox.addWidget(self.record_button)

        self.setLayout(vbox)

    def initDevices(self):
        """사용 가능한 오디오 입력 장치 목록을 가져와 콤보 박스에 추가합니다."""
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
    
    def start_recording(self):
        """녹음 시작 버튼을 눌렀을 때 호출됩니다."""
        device_index = self.device_combo.currentData()
        if device_index is None:
            QMessageBox.warning(self, "No Device Selected", "Please select a microphone.")
            return

        self.recorder = VoiceRecorder(device_index=device_index)
        self.recorder.finished.connect(self.on_recording_finished)
        self.recorder.error.connect(self.on_recording_error)

        self.status_label.setText("Recording...")
        self.record_button.setEnabled(False)
        self.recorder.start()

    def on_recording_finished(self, filepath):
        """녹음이 완료되었을 때 호출됩니다."""
        self.status_label.setText("Recording complete.")
        self.record_button.setEnabled(True)
        QMessageBox.information(self, "Recording Complete", f"File saved at:\n{filepath}")

    def on_recording_error(self, message):
        """녹음 중 오류가 발생했을 때 호출됩니다."""
        self.status_label.setText("Recording failed.")
        self.record_button.setEnabled(True)
        QMessageBox.critical(self, "Recording Error", f"An error occurred:\n{message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = JavisApp()
    ex.show()
    sys.exit(app.exec_())
