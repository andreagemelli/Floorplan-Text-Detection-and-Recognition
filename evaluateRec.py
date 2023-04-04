from collections import namedtuple
import numpy as np
import cv2
import os
import json
from difflib import SequenceMatcher
from scipy.optimize import linear_sum_assignment

def get_gt_pr(path_dir):
    gt=[]
    element=[]
    list_gt=os.listdir(path_dir)
    list_gt.sort()
    for dir in list_gt:
        element = []
        with open(os.path.join(path_dir, dir,'textes.txt'), 'r') as t:
            lines = t.readlines()
            for line in lines:
                splitted_line = line.strip().lower().split(',')
                text=splitted_line[3].strip().lower().split()
                try:
                    element.append(text[1])
                except:
                    element.append('')
            gt.append(element)
    return gt

def get_bag_of_words_from_json(pathJson):
    text_gt = []
    img = os.path.join('floorplans/dataset/test/test_json/', pathJson)
    with open(img) as f:
        data = json.load(f)
        for elem in data[0]['annotations']:
            text_gt.append(elem['text'])
    return text_gt

def evaluate_rec(gt_rec,pr_rec):
    accuracy = []
    min_accuracy = 0
    acc_i_j = []
    for i in range(len(pr_rec)):
        acc = 0
        acc_i_j = []
        for j in range(len(gt_rec)):
            acc = similar(pr_rec[i],gt_rec[j])
            acc_i_j.append(-acc)
        accuracy.append(acc_i_j)
    # implement maximize
    match_accuracy = linear_sum_assignment(accuracy)
    i = 0
    while (i < len(match_accuracy[0])):
        min_accuracy += (-accuracy[match_accuracy[0][i]][match_accuracy[1][i]])
        i += 1
    min_accuracy = min_accuracy / (len(pr_rec))
    return min_accuracy

def similar(a,b):
    return SequenceMatcher(None,a,b).ratio()

if __name__=="__main__":
    path_gt = 'floorplans/dataset/test/test_json'  # the same for image
    path_pr = 'floorplans/fine_tuning/fp_textes'
    lenght_gt = os.listdir(path_gt)
    lenght_gt.sort()
    list_gt = []
    list_pr = get_gt_pr(path_pr)
    accuracy_test = []

    for p in lenght_gt:
        list_gt.append(get_bag_of_words_from_json(p))

    for i in range(len(list_pr)):
        accuracy_test.append(evaluate_rec(list_gt[i],list_pr[i]))

    print(sum(accuracy_test) / len(list_pr))