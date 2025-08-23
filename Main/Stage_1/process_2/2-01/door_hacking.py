# door_hacking.py

import zipfile
import itertools
import string
import time
import multiprocessing as mp

# zip 파일 경로
ZIP_PATH = "/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_1/process_2/2-01/emergency_storage_key.zip"
PASSWORD_FILE = "password.txt"

charset = string.ascii_lowercase + string.digits
pwd_length = 6
total_attempts = len(charset) ** pwd_length
print_interval = 1_000_000  # 100만번마다 진행 상황 출력

def try_password(pwd):
    """zip 파일 비밀번호 테스트 (I/O 최소화)"""
    try:
        with zipfile.ZipFile(ZIP_PATH) as zf:
            # testzip()는 파일 CRC만 체크, 비밀번호가 맞으면 None 반환
            if zf.testzip() is None:
                return pwd
    except:
        return None
    return None

def password_worker(chunk):
    """멀티프로세싱용 worker, chunk 단위 처리"""
    for p in chunk:
        pwd = ''.join(p)
        result = try_password(pwd)
        if result:
            return result
    return None

def chunked_product(iterable, chunk_size):
    """generator로 itertools.product를 chunk 단위로 반환"""
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, chunk_size))
        if not chunk:
            return
        yield chunk

def unlock_zip():
    start_time = time.time()
    print(f"[INFO] Start cracking... Total possible: {total_attempts}")

    pool = mp.Pool(mp.cpu_count())
    attempts = 0

    # itertools.product generator
    product_gen = itertools.product(charset, repeat=pwd_length)

    # 멀티프로세싱 imap_unordered로 chunk 단위 처리
    chunk_size = 1000
    for result in pool.imap_unordered(password_worker, chunked_product(product_gen, chunk_size)):
        attempts += chunk_size
        if result:
            elapsed = time.time() - start_time
            print(f"[SUCCESS] Password found: {result}, total attempts: {attempts}, elapsed: {elapsed:.2f} sec")
            with open(PASSWORD_FILE, "w") as f:
                f.write(result)
            pool.terminate()
            return result
        if attempts % print_interval == 0:
            elapsed = time.time() - start_time
            print(f"[INFO] {attempts} attempts, elapsed: {elapsed:.2f} sec")

    pool.close()
    pool.join()
    print("[FAIL] Password not found")
    return None

if __name__ == "__main__":
    unlock_zip()
