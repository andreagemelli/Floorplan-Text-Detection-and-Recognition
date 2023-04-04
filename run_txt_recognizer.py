from txt_recognition.txt_recognizer import recognize
import os

def txt_recognizer(src, dest):
    for folder in os.listdir(src):
        img_name = os.path.splitext(os.path.basename(folder))[0]
        print(img_name)
        for crop in os.listdir(os.path.join(src, folder)):
            if crop.endswith(".jpg") or crop.endswith(".png"):
                crop_path = os.path.join(src, (img_name + "/" + crop))
                crop_txt = os.path.join(src, (img_name + "/crops.txt"))
                recognize(crop_path, crop_txt, img_name, dest)
