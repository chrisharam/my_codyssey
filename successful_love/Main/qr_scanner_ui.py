import cv2
import qrcode
import numpy as np
import threading
import time
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser

# GitHub URL
GITHUB_URL = "https://github.com/chrisharam/my_codyssey"
# 저장할 파일 경로
OUTPUT_FILE = 'qroutput.txt'

class QRCodeScannerApp:
    def __init__(self, root):
        """
        GUI 애플리케이션의 초기 설정을 담당합니다.
        """
        self.root = root
        self.root.title("실시간 QR 코드 스캐너")
        self.root.geometry("640x540")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # OpenCV QR 코드 감지기 초기화
        self.detector = cv2.QRCodeDetector()
        
        # 웹캠 연결 (0은 내장 웹캠)
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            messagebox.showerror("오류", "웹캠을 열 수 없습니다. 카메라가 연결되어 있는지 확인하거나 다른 장치를 시도하세요.")
            self.root.destroy()
            return
        
        self.last_detected_data = ""
        
        # UI 요소(비디오 라벨, 상태 라벨, 텍스트 박스) 생성
        self.setup_ui()
        
        # 출력 파일 초기화
        self.initialize_output_file()
        
        # 실시간 비디오 스트림 업데이트 루프 시작
        self.update_video_stream()

    def setup_ui(self):
        """
        Tkinter UI 요소들을 구성합니다.
        """
        # 비디오 프레임을 표시할 라벨 위젯
        self.video_label = tk.Label(self.root)
        self.video_label.pack(padx=10, pady=10)

        # 현재 상태를 표시할 라벨
        self.status_label = tk.Label(self.root, text="QR 코드를 기다리는 중...", font=("Helvetica", 12))
        self.status_label.pack(pady=5)

        # 인식된 내용을 표시할 텍스트 위젯
        self.text_box = tk.Text(self.root, height=10, width=70, state=tk.DISABLED, font=("Helvetica", 10))
        self.text_box.pack(pady=10)

        # 텍스트 박스용 스크롤바 추가
        self.scrollbar = tk.Scrollbar(self.root, command=self.text_box.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_box.config(yscrollcommand=self.scrollbar.set)
        
    def initialize_output_file(self):
        """
        프로그램 시작 시 출력 파일을 비웁니다.
        """
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, 'w') as f:
                f.write('')
        
    def update_video_stream(self):
        """
        웹캠에서 프레임을 읽어와 UI에 표시하고 QR 코드를 감지하는 메인 루프입니다.
        """
        ret, frame = self.cap.read()
        if not ret:
            self.status_label.config(text="웹캠 오류!", fg="red")
            return

        data, bbox, _ = self.detector.detectAndDecode(frame)
        
        if data:
            if data != self.last_detected_data:
                # 새로운 QR 코드가 인식되면 상태 라벨, 텍스트 박스, 파일 업데이트
                self.status_label.config(text=f"QR 코드 감지: {data}", fg="green")
                self.last_detected_data = data
                self.save_to_file(data)
                self.update_text_box(data)
                
                # 유튜브 또는 GitHub 링크라면 웹 브라우저 열기
                if "youtube.com" in data or "youtu.be" in data or "github.com" in data:
                    print(f"링크 감지: {data}, 브라우저를 엽니다.")
                    webbrowser.open(data)
                
            if bbox is not None:
                # 감지된 QR 코드 주위에 초록색 테두리 그리기
                bbox = bbox[0]
                cv2.polylines(frame, [bbox.astype(int)], isClosed=True, color=(0, 255, 0), thickness=2)
                
                # 인식된 데이터 텍스트를 화면에 오버레이
                text_position = (int(bbox[0][0]), int(bbox[0][1]) - 10)
                cv2.putText(frame, data, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            self.status_label.config(text="QR 코드를 기다리는 중...", fg="black")
            
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        
        self.video_label.imgtk = imgtk
        self.video_label.config(image=imgtk)

        self.root.after(10, self.update_video_stream)

    def save_to_file(self, data):
        """
        인식된 데이터를 qroutput.txt 파일에 추가합니다.
        """
        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {data}\n")
            
    def update_text_box(self, data):
        """
        GUI의 텍스트 박스에 인식된 내용을 추가합니다.
        """
        self.text_box.config(state=tk.NORMAL)
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        self.text_box.insert(tk.END, f"[{current_time}] {data}\n")
        self.text_box.see(tk.END)
        self.text_box.config(state=tk.DISABLED)

    def on_closing(self):
        """
        창이 닫힐 때 호출되며, 웹캠을 해제하고 창을 종료합니다.
        """
        if messagebox.askokcancel("종료", "프로그램을 종료하시겠습니까?"):
            self.cap.release()
            self.root.destroy()
            cv2.destroyAllWindows()

def create_and_display_qr_code(data):
    """
    주어진 데이터를 QR 코드로 변환하여 OpenCV 창에 표시합니다.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_np = np.array(img.convert('RGB'))
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    cv2.imshow("생성된 QR 코드 (아무 키나 누르면 닫힘)", img_bgr)
    
    # 이 창은 key 입력이 있을 때까지 대기
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # 라이브러리 설치 확인
    try:
        from PIL import Image, ImageTk
    except ImportError:
        messagebox.showerror("오류", "Pillow 라이브러리가 필요합니다. 'pip install Pillow'를 실행해주세요.")
        exit()
        
    # 멀티스레딩을 사용하여 두 함수를 동시에 실행
    scanner_thread = threading.Thread(target=lambda: QRCodeScannerApp(tk.Tk()))
    qr_creator_thread = threading.Thread(target=lambda: create_and_display_qr_code(GITHUB_URL))

    scanner_thread.start()
    qr_creator_thread.start()

    # mainloop는 scanner_thread 안에서 실행되므로 여기서 join을 기다릴 필요 없음
