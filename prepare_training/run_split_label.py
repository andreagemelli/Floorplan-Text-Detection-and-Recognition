import sys
#sys.path.insert(0,'/home/gemelli/dmp')
from txt_det.lib.prepare_training_data.split_label import split_label


if __name__ == "__main__":
    img_path = 'floorplans/dataset/augmented_img'
    json_path = 'floorplans/dataset/augmented_json'
    gt_path = 'floorplans/training/text_label'
    out_path = 'floorplans/training/re_image'
    label_tmp = 'floorplans/training/label_tmp'

    split_label(img_path, json_path, gt_path, out_path, label_tmp, exclude='_s')
