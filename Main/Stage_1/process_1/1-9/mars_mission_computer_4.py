import sys
import os
import time
import threading
import multiprocessing
import json

# 이 코드가 mars_mission_computer_3.py와 다른 폴더에 있다고 가정하고
# sys.path를 추가하여 import가 가능하도록 함
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '1-8')))
    from mars_mission_computer_3 import MissionComputer as parentClass
except ImportError:
    print("Failed to import MissionComputer from mars_mission_computer_3.py. Please ensure the path is correct.", file=sys.stderr, flush=True)
    sys.exit(1)

# 전역 상수 정의
INFO_LOG_PATH = './log/mission_info.json'
LOAD_LOG_PATH = './log/mission_load.json'

class MissionComputer(parentClass):
    """
    미션 컴퓨터 클래스. 부모 클래스인 MissionComputer의 기능을 상속받아
    시스템 로깅 및 부하 모니터링 기능을 추가합니다.
    """
    def __init__(self, instance_name=""):
        super().__init__()
        self.instance_name = instance_name
        # 로그 파일이 저장될 디렉토리 생성
        os.makedirs('log', exist_ok=True)
    
    # 시스템 정보 로깅
    def info_continuous(self, stop_event):
        """시스템 정보를 20초마다 연속적으로 로깅합니다."""
        while not stop_event.is_set():
            info = self.get_mission_computer_info()
            with open(INFO_LOG_PATH, 'a') as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {self.instance_name}\n") 
                f.write(json.dumps(info, indent=4) + '\n')
            print(f"[{time.strftime('%H:%M:%S')}] [{self.instance_name}] [INFO] System info saved.", flush=True)
            time.sleep(20)

    # 시스템 부하 로깅
    def load_continuous(self, stop_event):
        """시스템 부하를 20초마다 연속적으로 로깅합니다."""
        while not stop_event.is_set():
            load = self.get_mission_computer_load()
            with open(LOAD_LOG_PATH, 'a') as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {self.instance_name}\n")
                f.write(json.dumps(load, indent=4) + '\n')
            print(f"[{time.strftime('%H:%M:%S')}] [{self.instance_name}] [LOAD] System load saved.", flush=True)
            time.sleep(20)

    # 센서 데이터 출력
    def sensor_continuous(self, stop_event):
        """센서 데이터를 10초마다 5회 출력합니다."""
        count = 0
        while count < 5 and not stop_event.is_set():
            # 실제 센서 데이터를 가져오는 로직은 생략
            sensor_data = self.get_sensor_data()
            print(f"[{time.strftime('%H:%M:%S')}] [{self.instance_name}] [SENSOR] Sensor data placeholder output", flush=True)
            time.sleep(10)
            count += 1
        stop_event.set()


def run_thread_mode():
    """쓰레드 모드를 실행합니다."""
    runComputer = MissionComputer(instance_name="Thread-Instance")
    stop_event = threading.Event()

    t1 = threading.Thread(target=runComputer.info_continuous, args=(stop_event,))
    t2 = threading.Thread(target=runComputer.load_continuous, args=(stop_event,))
    t3 = threading.Thread(target=runComputer.sensor_continuous, args=(stop_event,))
    
    t1.start()
    t2.start()
    t3.start()

    try:
        print("\n쓰레드 모드 시작. 60초 후에 자동으로 중지됩니다.\n")
        time.sleep(60)
        stop_event.set()
    except KeyboardInterrupt:
        print("\n프로그램이 중단되었습니다.", flush=True)
        stop_event.set()

    t1.join()
    t2.join()
    t3.join()
    print("\n쓰레드 모드 종료.\n", flush=True)

def run_process_mode():
    """멀티프로세스 모드를 실행합니다."""
    stop_event = multiprocessing.Event()
    
    mc1 = MissionComputer(instance_name="Process-1")
    mc2 = MissionComputer(instance_name="Process-2")
    mc3 = MissionComputer(instance_name="Process-3")

    p1 = multiprocessing.Process(target=mc1.info_continuous, args=(stop_event,))
    p2 = multiprocessing.Process(target=mc2.load_continuous, args=(stop_event,))
    p3 = multiprocessing.Process(target=mc3.sensor_continuous, args=(stop_event,))

    p1.start()
    p2.start()
    p3.start()

    try:
        print("\n멀티프로세스 모드 시작. 60초 후에 자동으로 중지됩니다.\n")
        time.sleep(60)
        stop_event.set()
    except KeyboardInterrupt:
        print("\n프로그램이 중단되었습니다.", flush=True)
        stop_event.set()
    
    p1.join()
    p2.join()
    p3.join()
    print("\n멀티프로세스 모드 종료.\n", flush=True)


if __name__ == '__main__':
    while True:
        mode = input("choose your operation mode (thread/process): ").strip().lower()

        if mode == 'thread':
            run_thread_mode()
            break
        elif mode == 'process':
            run_process_mode()
            break
        else:
            print("Wrong input. Try again.\n", flush=True)
