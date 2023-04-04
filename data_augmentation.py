import os
import cv2
import json as js
from scipy import ndimage
import numpy as np

def check_img(img, json):
    base_name = os.path.splitext(os.path.basename(img))[0]
    img = cv2.imread(img)
    print(img.shape)
    w = img.shape[0]
    h = img.shape[1]
    data = js.load(open(json))
    boxes = data["annotations"]
    for box in boxes:
        x1 = box["x"]
        x2 = x1 + box["width"]
        y1 = box["y"]
        y2 = y1 + box["height"]
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    #horizontal_flip
    horizontal_img = cv2.flip(img, 1)
    cv2.imwrite('floorplans/dataset/augmented_img/001_h.jpg', horizontal_img)
    cv2.imshow("horizontal", horizontal_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #rotate
    rotated = ndimage.rotate(img, 270)
    cv2.imwrite('floorplans/dataset/augmented_img/001_r.jpg', rotated)
    cv2.imshow("rotation", rotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #stretch
    resized_h = cv2.resize(img, (int(w*2), int(h/2)))
    cv2.imwrite('floorplans/dataset/augmented_img/001_s.jpg', resized_h)
    cv2.imshow("stretch_h", resized_h)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''

def transform(img, json, aug_img_path, aug_json_path):
    def r(x, y, theta, ox, oy):
        s, c = np.sin(np.radians(theta)), np.cos(np.radians(theta))
        x, y = np.asarray(x) - ox, np.asarray(y) - oy
        return (x * c - y * s + ox) - (ox - oy), x * s + y * c + ox

    base_name = os.path.splitext(os.path.basename(img))[0]
    img = cv2.imread(img)
    h = img.shape[0]
    w = img.shape[1]
    data = js.load(open(json))
    boxes = data[0]["annotations"]

    #STRETCH

    stretched = cv2.resize(img, (int(w * 2), int(h / 2)))
    new = {}
    new['annotations'] = []
    new['class'] = "image"
    new['filename'] = (str(base_name) + "_s.jpg")
    for box in boxes:
        oldx1 = box["x"]
        oldx2 = oldx1 + box["width"]
        oldy1 = box["y"]
        oldy2 = oldy1 + box["height"]
        x = oldx1*2
        x2 = oldx2*2
        y = oldy1/2
        y2 = oldy2/2
        new['annotations'].append({
            "class": box["class"],
            "height": y2 - y,
            "text": box["text"],
            "width": x2 - x,
            "x": x,
            "y": y
        })

    with open((aug_json_path + base_name + '_s.json'), 'w') as outfile:
        js.dump(new, outfile)
    cv2.imwrite((aug_img_path + base_name + '_s.jpg'), stretched)

    # FLIP

    flipped = cv2.flip(img, 1)
    new = {}
    new['annotations'] = []
    new['class'] = "image"
    new['filename'] = (str(base_name) + "_f.jpg")
    for box in boxes:
        oldx1 = box["x"]
        oldx2 = oldx1 + box["width"]
        x2 = w - oldx1 - 1
        x1 = w - oldx2 - 1
        if x2 < x1:
            x1 = 0
        new['annotations'].append({
            "class": box["class"],
            "height": box["height"],
            "text": box["text"],
            "width": box["width"],
            "x": x1,
            "y": box["y"]
        })

    with open((aug_json_path + base_name + '_f.json'), 'w') as outfile:
        js.dump(new, outfile)
    cv2.imwrite((aug_img_path + base_name + '_f.jpg'), flipped)

    #ROTATE

    rotated = ndimage.rotate(img, 270, axes=(0, 1), reshape=True)
    new = {}
    new['annotations'] = []
    new['class'] = "image"
    new['filename'] = (str(base_name) + "_r.jpg")
    for box in boxes:
        oldx1 = box["x"]
        oldx2 = oldx1 + box["width"]
        oldy1 = box["y"]
        oldy2 = oldy1 + box["height"]
        x1, y1 = r(oldx1, oldy1, 90, w / 2, h / 2)
        x2, y2 = r(oldx2, oldy2, 90, w / 2, h / 2)
        new['annotations'].append({
            "class": box["class"],
            "height": box["width"],
            "text": box["text"],
            "width": box["height"],
            "x": x2,
            "y": y1
        })

    with open((aug_json_path + base_name + '_r.json'), 'w') as outfile:
        js.dump(new, outfile)
    cv2.imwrite((aug_img_path + base_name + '_r.jpg'), rotated)


if __name__ == "__main__":
    img_path = 'floorplans/dataset/images/'
    json_path = 'floorplans/dataset/json/'
    aug_img_path = 'floorplans/dataset/augmented_img/'
    aug_json_path = 'floorplans/dataset/augmented_json/'

    if not os.path.isdir(aug_img_path):
        os.mkdir(aug_img_path)
    if not os.path.isdir(aug_json_path):
        os.mkdir(aug_json_path)

    for json in os.listdir(json_path):
        base_name = os.path.splitext(os.path.basename(json))[0]
        print("Transforming image",base_name,"...")
        img = (img_path + base_name + '.jpg')
        json = (json_path + base_name + '.json')
        transform(img, json, aug_img_path, aug_json_path)

    '''
    for elem in ['_r','_s','_f']:
        debug_img = (aug_img_path + '094' + elem + '.jpg')
        debug_json = (aug_json_path + '094' + elem + '.json')
        check_img(debug_img, debug_json)
    '''


