import json
file = '/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_1/process_1/1-3/Mars_Base_Inventory_List.csv'
dataSet = []
sorted = []
try:
    with open(file, mode = 'r',encoding = 'utf-8') as f:
        next(f)
        for line in f:
            index = line.strip().split(',')
            if len(index) == 5:
                dataSet.append(index)
        
        print("\n"+"Before sorted")
        for item in dataSet:
            print(item)
        print("\n")
        dataSet.sort(key= lambda x: x[4],reverse= True)
        print("After sorted")
        for item in dataSet:
            print(item)
        print("\n")

        print("These are Flammability attribute which is over than 0.7 ")
        for item in dataSet:
            if float(item[4]) >=0.7:
                sorted.append(item)
                print(item)
        print('\n')
    
    output_path = '/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_1/process_1/1-3/Mars_Base_Inventory_danger.csv'
    with open(output_path,mode = 'w',encoding = 'utf-8') as wr:
        for line in dataSet:
            if len(line) == 5:
                wr.write(','.join(line)+'\n')
        print("Data file is written in file named 'Mars_Base_Inventory_danger.csv'")
        
        

except FileNotFoundError:
    print("File isn't found")
except UnicodeDecodeError:
    print("UTF-8 can't be used")
except PermissionError:
    print("Permission isn't allowed")