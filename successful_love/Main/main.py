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
GITHUB_URL_HARAM = "https://github.com/chrisharam/my_codyssey"
GITHUB_URL_YEJIN = "https://github.com/4yejin/codyssey"
# --- 새로운 GitHub 주소를 여기에 추가합니다. ---
GITHUB_URL_NEW = "https://www.infobank.net/"

# 저장할 파일 경로
OUTPUT_FILE = 'qroutput.txt'

class QRCodeScannerApp:
    def __init__(self, root):
        """
        GUI 애플리케이션의 초기 설정을 담당합니다.
        """
        self.root = root
        self.root.title("QR 코드 생성기 및 스캐너")
        self.root.geometry("1400x800")  # 창 크기를 더 넓게 설정
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # OpenCV QR 코드 감지기 초기화
        self.detector = cv2.QRCodeDetector()
        self.cap = None  # 카메라 객체 초기화
        self.last_detected_data = ""
        
        # UI 요소(비디오 라벨, QR 코드 라벨, 상태 라벨, 텍스트 박스) 생성
        self.setup_ui()
        
        # 출력 파일 초기화
        self.initialize_output_file()
        
        # 비디오 스트림은 '연결' 버튼 클릭 시 시작
        self.update_video_stream()

    def setup_ui(self):
        """
        Tkinter UI 요소들을 구성합니다.
        """
        # 전체 UI를 담는 메인 프레임
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 상단 프레임: 웹캠과 QR 코드들을 나란히 배치
        top_frame = tk.Frame(main_frame)
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 왼쪽 프레임: 웹캠 스캐너
        webcam_frame = tk.Frame(top_frame)
        webcam_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # URL 입력창과 연결 버튼 프레임
        control_frame = tk.Frame(webcam_frame)
        control_frame.pack(pady=5)
        
        # URL 입력 부분
        tk.Label(control_frame, text="IP 카메라 URL:", font=("Helvetica", 12)).pack(side=tk.LEFT)
        self.url_entry = tk.Entry(control_frame, width=40, font=("Helvetica", 10))
        self.url_entry.pack(side=tk.LEFT, padx=5)
        self.url_entry.insert(0, "http://<phone_ip_address>:<port>/video") # 예시 URL
        tk.Button(control_frame, text="연결", command=self.connect_to_camera).pack(side=tk.LEFT)
        
        # C타입 연결 버튼 추가
        tk.Button(control_frame, text="C타입으로 연결", command=self.connect_c_type_camera).pack(side=tk.LEFT, padx=(10, 0))

        tk.Label(webcam_frame, text="QR 코드 스캐너", font=("Helvetica", 14, "bold")).pack(pady=5)
        self.video_label = tk.Label(webcam_frame, width=640, height=480, relief="sunken", borderwidth=2) # 웹캠 크기 고정
        self.video_label.pack(fill=tk.BOTH, expand=True)

        # 오른쪽 프레임: QR 코드들
        qr_codes_container = tk.Frame(top_frame)
        qr_codes_container.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH)
        
        # 하람 GitHub QR 코드
        haram_qr_frame = tk.Frame(qr_codes_container)
        haram_qr_frame.pack(pady=10)
        tk.Label(haram_qr_frame, text="하람 GitHub", font=("Helvetica", 12)).pack()
        self.qr_label_haram = tk.Label(haram_qr_frame, bg="white", width=250, height=250)
        self.qr_label_haram.pack()

        # 예진 GitHub QR 코드
        yejin_qr_frame = tk.Frame(qr_codes_container)
        yejin_qr_frame.pack(pady=10)
        tk.Label(yejin_qr_frame, text="예진 GitHub", font=("Helvetica", 12)).pack()
        self.qr_label_yejin = tk.Label(yejin_qr_frame, bg="white", width=250, height=250)
        self.qr_label_yejin.pack()
        
        # 새로 추가된 GitHub QR 코드
        new_qr_frame = tk.Frame(qr_codes_container)
        new_qr_frame.pack(pady=10)
        tk.Label(new_qr_frame, text="새로운 GitHub", font=("Helvetica", 12)).pack()
        self.qr_label_new = tk.Label(new_qr_frame, bg="white", width=250, height=250)
        self.qr_label_new.pack()

        # QR 코드 이미지 생성 및 라벨에 표시
        self.create_qr_images()

        # 하단 프레임: 상태 및 결과 텍스트 박스
        bottom_frame = tk.Frame(main_frame)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        self.status_label = tk.Label(bottom_frame, text="카메라 연결을 기다리는 중...", font=("Helvetica", 12))
        self.status_label.pack(pady=5)

        self.text_box = tk.Text(bottom_frame, height=10, width=80, state=tk.DISABLED, font=("Helvetica", 10))
        self.text_box.pack(pady=10, fill=tk.BOTH, expand=True)

        # 텍스트 박스용 스크롤바 추가
        self.scrollbar = tk.Scrollbar(bottom_frame, command=self.text_box.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_box.config(yscrollcommand=self.scrollbar.set)
        
    def connect_to_camera(self):
        """
        입력된 URL로 카메라 연결을 시도합니다.
        """
        url = self.url_entry.get()
        if not url:
            messagebox.showwarning("경고", "IP 카메라 URL을 입력해주세요.")
            return

        # 기존 카메라가 있다면 해제
        if self.cap and self.cap.isOpened():
            self.cap.release()

        self.status_label.config(text="카메라에 연결 중...", fg="blue")
        self.root.update_idletasks() # UI 업데이트 강제

        try:
            self.cap = cv2.VideoCapture(url)
            if not self.cap.isOpened():
                messagebox.showerror("오류", f"카메라를 열 수 없습니다. URL을 확인하거나 다른 장치를 시도하세요: {url}")
                self.status_label.config(text="카메라 연결 실패", fg="red")
            else:
                self.status_label.config(text="카메라 연결 성공!", fg="green")
        except Exception as e:
            messagebox.showerror("오류", f"카메라 연결 중 오류가 발생했습니다: {e}")
            self.status_label.config(text="카메라 연결 실패", fg="red")

    def connect_c_type_camera(self):
        """
        C타입으로 연결된 카메라를 열려고 시도합니다.
        보통 0번 인덱스가 기본 웹캠이므로, 연결된 기기를 찾기 위해 시도합니다.
        """
        # 기존 카메라가 있다면 해제
        if self.cap and self.cap.isOpened():
            self.cap.release()
            
        self.status_label.config(text="C타입 카메라 연결 중...", fg="blue")
        self.root.update_idletasks()
        
        try:
            # 보통 C타입으로 연결된 기기는 0번이나 1번 인덱스를 가질 수 있습니다.
            # 여기서는 0번을 먼저 시도합니다.
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("오류", "C타입 카메라를 찾을 수 없습니다. 연결 상태를 확인해주세요.")
                self.status_label.config(text="C타입 카메라 연결 실패", fg="red")
            else:
                self.status_label.config(text="C타입 카메라 연결 성공!", fg="green")
        except Exception as e:
            messagebox.showerror("오류", f"카메라 연결 중 오류가 발생했습니다: {e}")
            self.status_label.config(text="카메라 연결 실패", fg="red")
            

    def create_qr_image(self, data, size=250):
        """
        주어진 데이터를 기반으로 QR 코드 이미지를 생성하고 반환합니다.
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # QR 코드 이미지를 생성하고 원하는 크기로 조정
        img_pil = qr.make_image(fill_color="black", back_color="white").resize((size, size), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image=img_pil)

    def create_qr_images(self):
        """
        하람, 예진, 새로운 GitHub QR 코드 이미지를 생성하여 라벨에 표시합니다.
        """
        try:
            # 하람 QR 코드 생성 및 표시
            img_tk_haram = self.create_qr_image(GITHUB_URL_HARAM)
            self.qr_label_haram.config(image=img_tk_haram)
            self.qr_label_haram.image = img_tk_haram  # GC 방지

            # 예진 QR 코드 생성 및 표시
            img_tk_yejin = self.create_qr_image(GITHUB_URL_YEJIN)
            self.qr_label_yejin.config(image=img_tk_yejin)
            self.qr_label_yejin.image = img_tk_yejin  # GC 방지
            
            # 새로 추가된 QR 코드 생성 및 표시
            img_tk_new = self.create_qr_image(GITHUB_URL_NEW)
            self.qr_label_new.config(image=img_tk_new)
            self.qr_label_new.image = img_tk_new # GC 방지
            
        except Exception as e:
            messagebox.showerror("QR 코드 생성 오류", f"QR 코드를 생성하는 중 오류가 발생했습니다: {e}")
            
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
        if self.cap is None or not self.cap.isOpened():
            # 카메라가 연결되지 않았거나 열리지 않았으면 업데이트를 중단
            self.status_label.config(text="카메라 연결 대기 중...", fg="black")
            self.root.after(100, self.update_video_stream)
            return

        ret, frame = self.cap.read()
        if not ret:
            self.status_label.config(text="웹캠 오류!", fg="red")
            self.root.after(100, self.update_video_stream)
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
        img_tk = ImageTk.PhotoImage(image=img)
        
        self.video_label.img_tk = img_tk
        self.video_label.config(image=img_tk)

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
            if self.cap is not None and self.cap.isOpened():
                self.cap.release()
            self.root.destroy()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    # 라이브러리 설치 확인
    try:
        from PIL import Image, ImageTk
    except ImportError:
        messagebox.showerror("오류", "Pillow 라이브러리가 필요합니다. 'pip install Pillow'를 실행해주세요.")
        exit()
        
    root = tk.Tk()
    app = QRCodeScannerApp(root)
    root.mainloop()

