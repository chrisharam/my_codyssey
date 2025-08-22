import sys
import os
import time
import threading
import multiprocessing
import json

# 이 코드가 mars_mission_computer_3.py와 다른 폴더에 있다고 가정하고
# sys.path를 추가하여 import가 가능하도록 함
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '1-8')))
from mars_mission_computer_3 import MissionComputer as parentClass

# 전역 상수 정의
INFO_LOG_PATH = '/workspaces/my_codyssey/Main/Stage_1/1-9/mission_info.json'
LOAD_LOG_PATH = '/workspaces/my_codyssey/Main/Stage_1/1-9/mission_load.json'

class MissionComputer(parentClass):
    def __init__(self):
        super().__init__()
        # 로그 파일이 저장될 디렉토리 생성
        os.makedirs('log', exist_ok=True)
    
    # 1회성 시스템 정보 로깅
    def info_once(self):
        # parentClass의 get_mission_computer_info를 호출하여 정보 가져오기
        info = self.get_mission_computer_info()
        with open(INFO_LOG_PATH, 'a') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
            f.write(json.dumps(info, indent=4) + '\n')
        print(f"[{time.strftime('%H:%M:%S')}] [INFO] System info saved.", flush=True)

    # 1회성 시스템 부하 로깅
    def load_once(self):
        # parentClass의 get_mission_computer_load를 호출하여 정보 가져오기
        load = self.get_mission_computer_load()
        with open(LOAD_LOG_PATH, 'a') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
            f.write(json.dumps(load, indent=4) + '\n')
        print(f"[{time.strftime('%H:%M:%S')}] [LOAD] System load saved.", flush=True)

    # 1회성 센서 데이터 출력 (실제 로직은 없음)
    def sensor_once(self):
        print(f"[{time.strftime('%H:%M:%S')}] [SENSOR] Sensor data placeholder output", flush=True)

def keep_going():
    print("\n" + "-"*50 + "\n", flush=True) 
    while True:
        try:
            user_op = input("Do you want to keep going? (y/n): ").strip().lower()
        except EOFError:
            return False
        if user_op == 'y':
            return True
        elif user_op == 'n':
            return False
        else:
            print("Please enter 'y' or 'n'.", flush=True)

# multiprocessing을 위한 함수는 if __name__ == '__main__': 블록 밖으로 이동
def run_info_proc(stop_event):
    mc = MissionComputer()
    while not stop_event.is_set():
        info = mc.get_mission_computer_info()
        with open(INFO_LOG_PATH, 'a') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
            f.write(json.dumps(info, indent=4) + '\n')
        print(f"[{time.strftime('%H:%M:%S')}] [INFO] System info saved.", flush=True)
        time.sleep(20)

def run_load_proc(stop_event):
    mc = MissionComputer()
    while not stop_event.is_set():
        load = mc.get_mission_computer_load()
        with open(LOAD_LOG_PATH, 'a') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
            f.write(json.dumps(load, indent=4) + '\n')
        print(f"[{time.strftime('%H:%M:%S')}] [LOAD] System load saved.", flush=True)
        time.sleep(20)

def run_sensor_proc(stop_event):
    mc = MissionComputer()
    count = 0
    while count < 5 and not stop_event.is_set():
        print(f"[{time.strftime('%H:%M:%S')}] [SENSOR] Sensor data placeholder output", flush=True)
        time.sleep(10)
        count += 1

if __name__ == '__main__':
    while True:
        mode = input("choose your operation mode (thread/process): ").strip().lower()

        if mode == 'thread':
            runComputer = MissionComputer()

            while True:
                t1 = threading.Thread(target=runComputer.info_once)
                t2 = threading.Thread(target=runComputer.load_once)
                t3 = threading.Thread(target=runComputer.sensor_once)

                t1.start()
                t2.start()
                t3.start()

                t1.join()
                t2.join()
                t3.join()
                
                if not keep_going():
                    break

            exit(0)

        elif mode == 'process':
            stop_event = multiprocessing.Event()
            
            p1 = multiprocessing.Process(target=run_info_proc, args=(stop_event,))
            p2 = multiprocessing.Process(target=run_load_proc, args=(stop_event,))
            p3 = multiprocessing.Process(target=run_sensor_proc, args=(stop_event,))

            p1.start()
            p2.start()
            p3.start()

            try:
                print("\nMultiprocessing started. Will auto-stop in 60 seconds...\n", flush=True)
                time.sleep(60)
                stop_event.set()
            except KeyboardInterrupt:
                print("\nProgram interrupted.", flush=True)
                stop_event.set()

            p1.join()
            p2.join()
            p3.join()
            exit(0)

        else:
            print("Wrong input. Try again.\n", flush=True)