import sys
import os
import zipfile
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class CCTVViewer(QWidget):
    def __init__(self, folder):
        super().__init__()
        self.folder = folder
        self.images = sorted([
            os.path.join(folder, f) for f in os.listdir(folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
        ])
        if not self.images:
            raise Exception("No images found in folder.")

        self.index = 0

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumSize(800, 600)  # 최소 크기 고정

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        self.setLayout(vbox)

        self.setWindowTitle("CCTV Image Viewer")
        self.resize(800, 600)
        self.show_image()

    def show_image(self):
        pixmap = QPixmap(self.images[self.index])
        label_size = self.label.size()
        scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled_pixmap)
        self.setWindowTitle(f"CCTV Image Viewer - {os.path.basename(self.images[self.index])}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.index = (self.index + 1) % len(self.images)
            self.show_image()
        elif event.key() == Qt.Key_Left:
            self.index = (self.index - 1) % len(self.images)
            self.show_image()
        elif event.key() == Qt.Key_Escape:
            self.close()

def unzip_cctv(zip_path, extract_to):
    if not os.path.exists(extract_to):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Extracted {zip_path} to {extract_to}")
    else:
        print(f"{extract_to} already exists. Skipping extraction.")

if __name__ == "__main__":
    zip_file = "/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey-2/Main/Stage_1/process_2/2-9/cctv.zip"
    extract_folder = "CCTV"

    unzip_cctv(zip_file, extract_folder)

    app = QApplication(sys.argv)
    viewer = CCTVViewer(extract_folder)
    viewer.show()
    sys.exit(app.exec_())
