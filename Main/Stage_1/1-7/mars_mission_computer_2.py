import sys
import os
import time
import json
import threading
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '1-6')))
from mars_mission_computer import DummySensor
print(os.path)
# class MissionComputer:
#     def __init__(self):
#         self.env_values = {
#             'mars_base_internal_temperature' : None,
#             'mars_base_external_temperature': None,
#             'mars_base_internal_humidity': None,
#             'mars_base_external_illuminance': None,
#             'mars_base_internal_co2': None,
#             'mars_base_internal_oxygen': None
#         }
#         self.exit_flag = False

#     def get_sensor_data(self):
#         ds = DummySensor()   #instanciation   

#         thread = threading.Thread(target = self.exit_thread, daemon = True)  
#         thread.start()

#         while not self.exit_flag:
#             ds.set_env() #set random values for variables
#             self.env_values = ds.get_env()
#             time.sleep(5)
#             print(json.dumps(self.env_values, indent = 4))
#             print("-" * 40)    
            
#     def exit_thread(self):
#         while True:
#             user_input = input("\nTry to enter 'exit' anytime you want to escape.\n").strip().lower()
#             if user_input == 'exit':
#                 print("Exiting..")
#                 self.exit_flag = True
#                 break
    
# RunComputer = MissionComputer()
# RunComputer.get_sensor_data()