file = '/workspaces/my_codyssey/Main/mission_computer_main.log'
log_analysis = ['log file downloaded. But there are some strange things.',
                '-------------------------------------------------------',
                '2023-08-27 11:35:00,INFO,Oxygen tank unstable.',
                '--> some dangerous signals...',
                '2023-08-27 11:40:00,INFO,Oxygen tank explosion.',
                '--> there must be danger.',
                '2023-08-27 12:00:00,INFO,Center and mission control systems powered down.',
                '--> Power down and that we must do something.'
                ]
try:
    with open(file, mode= 'r', encoding = 'utf-8') as f:
        print(f.read())

    with open("log_analysis_markdown", mode='a', encoding = 'utf-8') as mk:
        for line in log_analysis:
            mk.write(line + '\n')

except FileNotFoundError:
    print("File isn't found")
except UnicodeDecodeError:
    print("UTF-8 can't be used")
except PermissionError:
    print("Permission isn't allowed")