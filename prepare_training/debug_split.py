import cv2
import os, random


if __name__ == "__main__":
    json_path = 'floorplans/dataset/json'
    jsons = os.listdir(json_path)
    json_file = random.choice(jsons)
    _, basename = os.path.split(json_file)
    file_name = basename.split(".")[0]

    img = cv2.imread(("floorplans/training/re_image/" + str(file_name) + ".jpg"))
    with open(("floorplans/training/label_tmp/" + str(file_name) + ".txt"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            splitted_line = line.strip().lower().split()
            x1, y1, x2, y2 = int(float(splitted_line[1]) + 1), int(float(splitted_line[2]) + 1), \
                             int(float(splitted_line[3]) + 1), int(float(splitted_line[4]) + 1)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)

        cv2.imshow('prova',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
