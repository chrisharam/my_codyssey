import numpy as np

try:
    arr1 = np.genfromtxt('/workspaces/my_codyssey/Main/1-5/mars_base_main_parts-001.csv',dtype=None,names = True,encoding='utf-8-sig',delimiter=',')
    arr2 = np.genfromtxt('/workspaces/my_codyssey/Main/1-5/mars_base_main_parts-002.csv',dtype=None,names = True,encoding='utf-8-sig',delimiter=',') 
    arr3 = np.genfromtxt('/workspaces/my_codyssey/Main/1-5/mars_base_main_parts-003.csv',dtype=None,names = True,encoding='utf-8-sig',delimiter=',')

    parts = np.concatenate((arr1,arr2,arr3))
    mean_strength = np.mean(parts['strength'])
    below_things = parts[parts['strength'] < mean_strength]

    np.savetxt('/workspaces/my_codyssey/Main/1-5/parts_to_work_on.csv',
               below_things,
               delimiter=',',
               fmt='%s,%d',
               header='part,strength'
               )    
    
    print("Session completed."+"\n")
    print(f"average : {round(mean_strength,3)}")
    

except OSError as e:
    print(f"file error:{e}")

