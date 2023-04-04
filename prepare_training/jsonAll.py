from json_to_txt import json_to_txt
import os

if __name__ == "__main__":
    global_path='floorplans/dataset/json'
    exclude = '_s'
    list_json = os.listdir(global_path)
    list_json.sort()

    for p in list_json:
        if exclude not in p:
            print(p)
            json_to_txt(global_path, p)
