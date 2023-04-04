import os
import sys
from txt_det.ctpn.detect import detect
from crop_imgs import crop_imgs
from run_txt_recognizer import txt_recognizer

if __name__ == "__main__":
    # change checkpoint path into txt_det/ctpn/text.yml too
    checkpoint_path = "/checkpoints/yeah"
    dataset_path = "floorplans/yeah"
    train = checkpoint_path.split("/")[2] #ex.first_train

    dest_path = "floorplans/" + train
    detections_path = (dest_path + "/fp_detections")
    crops_path = (dest_path + "/fp_crops")
    textes_path = (dest_path + "/fp_textes")

    if not os.path.isdir(dest_path):
        os.mkdir(dest_path)
    if not os.path.isdir(detections_path):
        os.mkdir(detections_path)
    if not os.path.isdir(crops_path):
        os.mkdir(crops_path)
    if not os.path.isdir(textes_path):
        os.mkdir(textes_path)

    mode = sys.argv[1]
    
    if mode == 'detect':
        detect(src=dataset_path, dest=detections_path, check_p=checkpoint_path)
    elif mode == 'crop':
        crop_imgs(imgs=dataset_path, src=detections_path, dest=crops_path)
    elif mode == 'rec':
        txt_recognizer(src=crops_path, dest=textes_path)
    else:
        print('Choose a mode: [detect, crop, rec]')
    print("Finished succesfully")
