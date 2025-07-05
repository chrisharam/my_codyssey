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
        os.makedirs('log', exist_ok=True)

    #load info-data for one-time
    def info_once(self):
        info = self.get_mission_computer_info()
        with open(INFO_LOG_PATH, 'a') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
            f.write(json.dumps(info, indent=4) + '\n')
        print(f"[{time.strftime('%H:%M:%S')}] [INFO] System info saved.", flush=True)

    #load data for one-time
    def load_once(self):
        load = self.get_mission_computer_load()
        with open(LOAD_LOG_PATH, 'a') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
            f.write(json.dumps(load, indent=4) + '\n')
        print(f"[{time.strftime('%H:%M:%S')}] [LOAD] System load saved.", flush=True)

    #print data for one-time
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
                
                #after work is done, wait until user's input whether keep going or not
                if not keep_going():
                    break

            exit(0)

        elif mode == 'process':
            stop_event = multiprocessing.Event()

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