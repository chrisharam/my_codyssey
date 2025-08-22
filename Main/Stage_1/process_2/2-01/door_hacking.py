# ===============================================
# Google Colab: GPU 기반 Zip 패스워드 크래킹
# ===============================================

# 1) 시스템 업데이트 & 필수 도구 설치
!apt-get update -qq
!apt-get install -y hashcat p7zip-full john -qq  # hashcat + zip2john
!hashcat --version

# 2) GitHub에서 프로젝트 클론 (사용자 repo로 교체!)
!rm -rf my_codyssey
!git clone https://github.com/<YOUR_GITHUB_ID>/<YOUR_REPO>.git my_codyssey

# 3) 압축파일 경로 설정
ZIP_PATH = "/content/my_codyssey/Main/Stage_1/process_2/2-01/emergency_storage_key.zip"
HASH_PATH = "/content/zip.hash"
PASSWORD_FILE = "/content/my_codyssey/Main/Stage_1/process_2/2-01/password.txt"

# 4) zip → hashcat용 해시 추출
!zip2john "{ZIP_PATH}" > {HASH_PATH}
!head -n 5 {HASH_PATH}

# 5) hashcat 실행
# -m 값: ZIP 포맷에 따라 다름
#   PKZIP (legacy): 17200
#   WinZip AES: 13600
#   일반 PKZIP + 암호: 17225 등
# (우선 17200부터 시도, 안되면 다른 모드 확인 필요)
!hashcat -m 17200 -a 3 {HASH_PATH} -1 ?l?d '?1?1?1?1?1?1' --force --status --status-timer=60 --machine-readable --potfile-path=/content/hashcat.potfile

# 6) 크래킹된 비밀번호 확인
!hashcat -m 17200 {HASH_PATH} --show --potfile-path=/content/hashcat.potfile > {PASSWORD_FILE}
!cat {PASSWORD_FILE}

print("✅ Password cracking attempt finished. Check password.txt")
