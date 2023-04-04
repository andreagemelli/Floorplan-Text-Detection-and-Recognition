from collections import namedtuple
import numpy as np
import cv2
import os
import json
from scipy.optimize import linear_sum_assignment

def bb_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA =max(int(boxA[0]), int(boxB[0]))
    yA =max(int(boxA[1]), int(boxB[1]))
    xB =min(int(boxA[2]), int(boxB[2]))
    yB =min(int(boxA[3]), int(boxB[3]))

    # compute the area of intersection rectangle
    if((int(boxA[2])<int(boxB[0])) or (int(boxB[2])<int(boxA[0]))):
        interArea=0
    else:
        interArea = (xB - xA + 1) * (yB - yA + 1)

    # compute the area of both the prediction and ground-truth
    # rectangles

    boxAArea = (int(boxA[2]) - int(boxA[0]) + 1) * (int(boxA[3]) - int(boxA[1]) + 1)
    boxBArea = (int(boxB[2]) - int(boxB[0]) + 1) * (int(boxB[3]) - int(boxB[1]) + 1)

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
    # return the intersection over union value
    return iou

def get_gt_pr(path_dir):
    gt=[]
    element=[]
    list_gt=os.listdir(path_dir)
    list_gt.sort()
    for dir in list_gt:
        if dir.endswith(".txt"):
            element=[]
            with open(os.path.join(path_dir, dir), 'r') as t:
                print(os.path.join(path_dir, dir))
                lines = t.readlines()
                for line in lines:
                    splitted_line = line.strip().lower().split(',')
                    element.append(splitted_line)
                gt.append(element)
    return gt

def get_txt_from_json(pathJson):
    bboxes = []
    img = os.path.join('floorplans/dataset/test/test_json/', pathJson)
    with open(img) as f:
        data = json.load(f)
        for elem in data[0]['annotations']:
            box=[]
            box.append(int(elem['x']))
            box.append(int(elem['y']))
            box.append(int(elem['x']+elem['width']))
            box.append(int(elem['y']+elem['height']))
            bboxes.append(box)
    return bboxes


def evaluate_floorplans(img_pr,img_gt):
    accuracy=[]
    min_accuracy=0
    acc_i_j=[]
    for i in range(len(img_pr)):
        acc=0
        acc_i_j=[]
        for j in range(len(img_gt)):
            acc=bb_intersection_over_union(img_pr[i],img_gt[j])
            acc_i_j.append(-acc)
        accuracy.append(acc_i_j)
    #implement maximize
    match_accuracy=linear_sum_assignment(accuracy)
    i=0
    while(i<len(match_accuracy[0])):
        min_accuracy+=(-accuracy[match_accuracy[0][i]][match_accuracy[1][i]])
        i+=1
    if(len(img_pr)<len(img_gt)):
        min_accuracy=min_accuracy/(len(img_gt))
    else:
        min_accuracy=min_accuracy/(len(img_pr))
    return min_accuracy

if __name__=="__main__":
    path_gt = 'floorplans/dataset/test/test_json'  # the same for image
    path_pr = 'floorplans/fine_tuning/fp_detections'

    lenght_gt=os.listdir(path_gt)
    lenght_gt.sort()
    list_gt=[]
    list_pr=get_gt_pr(path_pr)
    accuracy_test=[]

    for p in lenght_gt:
        list_gt.append(get_txt_from_json(p))

    #the lenght of gt and pr list are the same
    for i in range(len(list_pr)):
        accuracy_test.append(evaluate_floorplans(list_gt[i],list_pr[i]))
    print(sum(accuracy_test)/len(list_pr))





