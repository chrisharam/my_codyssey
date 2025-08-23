import qrcode
import os
import cv2
import numpy as np
from PIL import Image

def create_and_display_qr_code(data, file_name="my_qrcode.png"):
    """
    주어진 데이터를 QR 코드로 변환하여 이미지 파일로 저장하고,
    OpenCV를 사용하여 화면에 표시합니다.

    :param data: QR 코드로 변환할 문자열 (URL, 텍스트 등)
    :param file_name: 저장할 이미지 파일 이름
    """
    
    # QR 코드 객체 생성
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # QR 코드로 변환할 데이터 추가
    qr.add_data(data)
    qr.make(fit=True)
    
    # 이미지 파일 생성
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 파일 저장
    img.save(file_name)
    print(f"'{file_name}' 파일로 QR 코드가 생성되었습니다.")
    
    # Pillow 이미지 객체를 NumPy 배열(OpenCV 이미지 형식)로 변환
    img_np = np.array(img.convert('RGB'))
    
    # BGR 형식으로 변환 (OpenCV는 BGR 형식을 사용)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # 생성된 QR 코드 이미지를 화면에 출력
    cv2.imshow("QR Code", img_bgr)
    
    print("QR 코드 창이 열렸습니다. 아무 키나 누르면 창이 닫힙니다.")
    
    # 아무 키나 누를 때까지 대기
    cv2.waitKey(0)
    
    # 창 닫기
    cv2.destroyAllWindows()
    print("창이 닫혔습니다.")

if __name__ == "__main__":
    # GitHub URL
    github_url = "https://github.com/chrisharam/my_codyssey"
    
    # 함수 실행: QR 코드 생성 및 화면 출력
    create_and_display_qr_code(github_url)
