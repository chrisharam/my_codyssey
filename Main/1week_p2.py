file = '/workspaces/my_codyssey/Main/mission_computer_main.log'
dataSet = []
try:
    with open(file, mode= 'r', encoding = 'utf-8') as f:
        next(f)
        for line in f:
            index = line.strip().split(',')
            if len(index) == 3:
                dataSet.append(index)

except FileNotFoundError:
    print("File isn't found")
except UnicodeDecodeError:
    print("UTF-8 can't be used")
except PermissionError:
    print("Permission isn't allowed")
    
print("Data Set values are below\n")
for row in dataSet:
    print(row)