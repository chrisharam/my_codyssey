import csv

area_struct_path ="/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_2/process_3/3-01/area_struct.csv"
area_map_path = "/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_2/process_3/3-01/area_map.csv"
area_category_path = "/Users/jeongharam/SW_CAMP_PROJECT/my_codyssey/Main/Stage_2/process_3/3-01/area_category.csv"

area_map_data = {}
area_category_data = {}
area_struct_data = []

try:
    with open(area_map_path,"r",encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            x, y, mountain = int(line[0]), int(line[1]), int(line[2])
            if mountain == 1:
                mountain = "O"
            else:
                mountain = "X"
            area_map_data[(x,y)] = mountain
        print("\narea_map_data dictionanry undertakes key(x,y) and value(mountaion)")

    with open(area_category_path,"r",encoding = "utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            area_category_data[int(line[0])] = line[1]
        print("\narea_category_data dictionary undertakes key(category) and value(struct).")

    with open(area_struct_path, "r",encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            x,y,category,area = int(line[0]),int(line[1]), int(line[2]),int(line[3])
            mountain = area_map_data.get((x,y), 0)
            struct = area_category_data.get(category,"NONE")
            #dictionary in list
            area_struct_data.append({
                "x" : x,
                "y" : y,
                "area" : area,
                "mountain" : mountain,
                "category": category,
                "struct" : struct
            })
        print("\nTotal data is merged in area_struct_data")

        print("\n"+80*"-")
        print("\n[Selected 10 Data from Merged Data]")
        for item in area_struct_data[:10]:
            print(item)

        print("\n"+80*"-")
        print("\n[Area 1 Data]")
        for item in area_struct_data:
            if item["area"] == 1:
                print(item)


except FileNotFoundError:
    print("Error: File not found")
except UnicodeDecodeError:
    print("Error regarding Unicode")
except Exception as e:
    print("Unknown error:", e)