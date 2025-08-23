import itertools
import string
import zipfile
import multiprocessing as mp
import time
import sys

# 파일 경로
ZIP_PATH = "/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_1/process_2/2-01/emergency_storage_key.zip"
PASSWORD_FILE = "/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_1/process_2/2-01/password.txt"

# 문자 집합: 소문자 + 숫자 + 대문자
CHARSET = string.ascii_lowercase + string.digits + string.ascii_uppercase
PREFIX_LENGTH = 2
SUFFIX_LENGTH = 4
REPORT_INTERVAL = 10_000_000  # 1천만 번 시도마다 출력

def save_password(password):
    """비밀번호를 파일에 저장"""
    try:
        with open(PASSWORD_FILE, "w") as f:
            f.write(password)
    except Exception as e:
        print(f"[ERROR] Failed to save password: {e}")

def worker(prefix_chunk, total_tasks, start_time, found, attempts):
    """멀티프로세스 작업자 - 각 프로세스가 독립적으로 작업 수행"""
    try:
        with zipfile.ZipFile(ZIP_PATH) as zf:
            local_attempts = 0
            
            for prefix_chars in prefix_chunk:
                if found.value:
                    return
                prefix_str = ''.join(prefix_chars)

                for suffix_chars in itertools.product(CHARSET, repeat=SUFFIX_LENGTH):
                    if found.value:
                        return
                    
                    candidate = prefix_str + ''.join(suffix_chars)
                    local_attempts += 1
                    
                    # 1천만 번 시도마다 공유 변수 업데이트 및 출력
                    if local_attempts % REPORT_INTERVAL == 0:
                        with attempts.get_lock():
                            attempts.value += REPORT_INTERVAL
                            elapsed = time.time() - start_time
                            progress = (attempts.value / total_tasks) * 100
                            sys.stdout.write(f"\r[INFO] {attempts.value} attempts ({progress:.2f}%), elapsed: {elapsed:.2f} sec")
                            sys.stdout.flush()

                    try:
                        zf.setpassword(candidate.encode())
                        if zf.testzip() is None:
                            print(f"\n[SUCCESS] Password found: {candidate}")
                            save_password(candidate)
                            found.value = True
                            return
                    except Exception:
                        pass # 압축 오류는 무시

    except Exception as e:
        print(f"[ERROR][Worker] {e}")

def unlock_zip():
    """ZIP 암호 해독 메인 함수"""
    try:
        total_attempts = len(CHARSET) ** (PREFIX_LENGTH + SUFFIX_LENGTH)
        start_time = time.time()
        print("[INFO] Start cracking...")
        print(f"[INFO] Charset size: {len(CHARSET)}, Total possible: {total_attempts}")

        # 멀티프로세스 공유 변수
        found = mp.Value('b', False)
        attempts = mp.Value('i', 0)

        # 앞 2자리 조합 생성 및 CPU 코어 수로 분할
        prefixes = list(itertools.product(CHARSET, repeat=PREFIX_LENGTH))
        
        # 컴퓨터 과열을 막기 위해 코어 수를 조절할 수 있습니다 (예: mp.cpu_count() - 2)
        num_proc = mp.cpu_count()
        chunk_size = len(prefixes) // num_proc
        prefix_chunks = [prefixes[i*chunk_size:(i+1)*chunk_size] for i in range(num_proc)]
        if len(prefixes) % num_proc != 0:
            prefix_chunks[-1].extend(prefixes[num_proc*chunk_size:])

        # 프로세스 실행
        processes = []
        for chunk in prefix_chunks:
            p = mp.Process(target=worker, args=(chunk, total_attempts, start_time, found, attempts))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        if not found.value:
            print("\n[FAIL] Password not found in given charset.")
        else:
            elapsed = time.time() - start_time
            print(f"[DONE] Elapsed time: {elapsed:.2f} sec")

    except FileNotFoundError:
        print(f"[ERROR] ZIP file not found at {ZIP_PATH}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")

if __name__ == "__main__":
    unlock_zip()