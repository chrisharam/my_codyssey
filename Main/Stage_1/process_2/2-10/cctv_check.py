import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2

class CCTVCheck(QWidget):
    def __init__(self, folder):
        super().__init__()
        self.folder = folder

        # 이미지 파일만 필터링
        self.images = sorted([
            os.path.join(folder, f) for f in os.listdir(folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
        ])
        if not self.images:
            raise Exception("No images found in folder.")

        self.index = 0
        self.found_person = False

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumSize(800, 600)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setWindowTitle("CCTV Person Detector")
        self.resize(800, 600)

        # OpenCV HOG 사람 검출기 초기화
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        self.process_next_image()

    def process_next_image(self):
        self.found_person = False

        while self.index < len(self.images):
            img_path = self.images[self.index]
            img = cv2.imread(img_path)
            if img is None:
                print(f"Failed to load image: {img_path}")
                self.index += 1
                continue

            # OpenCV는 BGR, PyQt는 RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # 사람 검출
            rects, _ = self.hog.detectMultiScale(img_rgb, winStride=(8,8))

            if len(rects) > 0:
                self.found_person = True

                # QImage 생성
                height, width, channel = img_rgb.shape
                bytes_per_line = 3 * width
                qimg = QImage(img_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)

                # QPixmap 변환 및 라벨에 출력
                pixmap = QPixmap.fromImage(qimg)
                scaled_pixmap = pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.label.setPixmap(scaled_pixmap)

                self.setWindowTitle(f"CCTV Person Detector - Person found in {os.path.basename(img_path)}")
                break
            else:
                self.index += 1

        if not self.found_person:
            QMessageBox.information(self, "검색 종료", "모든 사진을 검색했습니다. 사람을 찾지 못했습니다.")
            self.close()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if self.found_person:
                self.index += 1
            self.process_next_image()
        elif event.key() == Qt.Key_Escape:
            self.close()

if __name__ == "__main__":
    folder = "/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_1/process_2/2-09/CCTV"

    app = QApplication(sys.argv)
    window = CCTVCheck(folder)
    window.show()
    sys.exit(app.exec_())
