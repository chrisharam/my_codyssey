import sys
import os
import time
import json
import threading
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '1-6')))
from mars_mission_computer import DummySensor

class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature' : None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }
        self.exit_flag = False

        self.env_history = {
            key: [] for key in self.env_values
        } #value storing organized by list

    def get_sensor_data(self):
        ds = DummySensor()   #instanciation   

        thread = threading.Thread(target = self.exit_thread, daemon = True)  
        thread.start()

        count = 0

        while not self.exit_flag:
            ds.set_env() #set random values for variables
            self.env_values = ds.get_env()
            time.sleep(5)
            print(json.dumps(self.env_values, indent = 4))
            print("-" * 40)    
            
            #cumulation of values for calculating average per 5 minutes
            for key in self.env_values:
                self.env_history[key].append(self.env_values[key])

            count += 1
            if count == 60:
                print("average of 5 minutes.\n")
                # there are 6 columns, each column account for different data type
                avg = {} #dictionary for storing 5-mitues average values
                for key in self.env_history:
                    avg[key] = round(sum(self.env_history[key])/len(self.env_history[key]),4)
                print(json.dumps(avg, indent = 4))
                print("="*40)

                self.env_history = {key : [] for key in self.env_values}
                count = 0

    def exit_thread(self):
        while True:
            user_input = input("\nTry to enter 'exit' anytime you want to escape.\n").strip().lower()
            if user_input == 'exit':
                print("System stopped..")
                self.exit_flag = True
                break
    
RunComputer = MissionComputer()
RunComputer.get_sensor_data()