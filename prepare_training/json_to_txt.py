import json
import os

def json_to_txt(global_path, pathJson):
    bboxes = []
    img = os.path.join(global_path, pathJson)
    with open(img) as f:
        data = json.load(f)
        if 'augmented' in global_path:
            annotations = data['annotations']
        else:
            annotations = data[0]['annotations']
        for elem in annotations:
            #print(elem)
            cb = []
            cb.append(elem['x'])
            cb.append(elem['y'])
            cb.append(elem['width'])
            cb.append(elem['height'])
            bboxes.append(cb)

    #print(bboxes)
    base_name = os.path.splitext(os.path.basename(img))[0]
    if not os.path.isdir('floorplans/training'):
        os.mkdir('floorplans/training')
    dest_path = ('floorplans/training/text_label/')
    if not os.path.isdir(dest_path):
        os.mkdir(dest_path)
    dest = os.path.join(dest_path, ('gt_' + base_name + '.txt'))

    with open(dest, 'w') as f:
        for bb in bboxes:
            line = (str(bb[0]) + ',' + str(bb[1]) + ',' + str(bb[0] + bb[2]) + ',' + str(bb[1]) + ',' +
                    str(bb[0]) + ',' + str(bb[1] + bb[3]) + ',' + str(bb[0] + bb[2]) + ',' +
                    str(bb[1] + bb[3]))
            f.write(line)
            f.write("\n")
