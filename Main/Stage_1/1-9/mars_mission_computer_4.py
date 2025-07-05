# Multiprocessing: 각 프로세스는 독립된 공간(인스턴스 간 변수,객체상태 공유x)
# main파일에서 선언된 객체구조가 인스턴스를 만드는 공간이, 서로에게 영향을 미치지 않는 독립된 메모리 공간에 할당됨.
# 이때 다른 공간의 process가 시작될 때, main모듈이 실행되어 계속하여 다른 인스턴스를 만드는 무한루프가 발생할 수 있음
# 이를 방지하고자, if __name__ == ‘__main__’을 명시적으로 main에서 구현하여 main에서만 process를 만들도록 함

# MultiThread: 여러 스레드가 하나의 프로세스에서 실행(인스턴스 간 변수, 객체상태 공유 0)
# 하나의 메모리 공간에서 여러 개의 인스턴스를 만듦. 이때 여러 개의 인스턴스는 하나의 메모리에서 사용되기에 자원을 할당받아
# 기능을 수행하게 됨.

import sys
import os
import time
import threading
import multiprocessing
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '1-8')))
from mars_mission_computer_3 import MissionComputer as parentClass

INFO_LOG_PATH = '/workspaces/my_codyssey/Main/Stage_1/1-9/mission_info.json'
LOAD_LOG_PATH = '/workspaces/my_codyssey/Main/Stage_1/1-9/mission_load.json'
class MissionComputer(parentClass):
    def __init__(self):
        super().__init__()
        os.makedirs('log', exist_ok=True)  # 로그 저장 폴더

    def repeat_info(self, interval=20):
        while True:
            info = self.get_mission_computer_info()
            with open(INFO_LOG_PATH, 'a') as f:
                f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
                f.write(json.dumps(info, indent=4) + '\n')
            time.sleep(interval)

    def repeat_load(self, interval=20):
        while True:
            load = self.get_mission_computer_load()
            with open(LOAD_LOG_PATH, 'a') as f:
                f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
                f.write(json.dumps(load, indent=4) + '\n')
            time.sleep(interval)

    def get_sensor_data(self):
        count = 0
        while count < 5:
            print(f"[{time.strftime('%H:%M:%S')}] Sensor data placeholder output")
            time.sleep(10)
            count += 1


#For multi-thread
def run_info(mc_instance):
    mc_instance.repeat_info()

def run_load(mc_instance):
    mc_instance.repeat_load()

def run_sensor(mc_instance):
    mc_instance.get_sensor_data()


#Multi-thread methods
def run_info_proc():
    mc = MissionComputer()
    mc.repeat_info()

def run_load_proc():
    mc = MissionComputer()
    mc.repeat_load()

def run_sensor_proc():
    mc = MissionComputer()
    mc.get_sensor_data()

#if Operation is on this file, Do this statement.
if __name__ == '__main__':
    mode = 'thread'  

    if mode == 'thread':
        runComputer = MissionComputer()
        t1 = threading.Thread(target=run_info, args=(runComputer,), daemon=True)
        t2 = threading.Thread(target=run_load, args=(runComputer,), daemon=True)
        t3 = threading.Thread(target=run_sensor, args=(runComputer,), daemon=True)

        t1.start()
        t2.start()
        t3.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print('Program interrupted.')

    elif mode == 'process':
        p1 = multiprocessing.Process(target=run_info_proc)
        p2 = multiprocessing.Process(target=run_load_proc)
        p3 = multiprocessing.Process(target=run_sensor_proc)

        p1.start()
        p2.start()
        p3.start()

        p1.join()
        p2.join()
        p3.join()
