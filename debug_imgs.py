import cv2
import os


def debug_imgs(src):
    src_img = src + '/fp_detections'
    src_textes = src + '/fp_textes'
    debug = src + '/debug'
    if not os.path.isdir(debug):
        os.mkdir(debug)
    for img in os.listdir(src_img):
        if (img.endswith(".jpg") or img.endswith(".png")) and '36' in img:
            base_name = os.path.splitext(os.path.basename(img))[0]
            print("Debugging...",base_name)
            img = cv2.imread(os.path.join(src_img, img))
            # cv2.imshow("image",img)
            # x=os.path.join(src_textes,base_name)
            with open(os.path.join(src_textes,  base_name, "textes.txt"), "r") as tc:
                content=tc.readlines()
                for box in content:
                    x1, y1, x2, y2 = box.split(',')
                    a = str(y2)
                    try:
                        b, txt = a.split()
                    except:
                        b = a.split()[0]
                        #print(b)
                        txt = ''

                    cv2.putText(img, txt, ((int(x1)), (int(b) + 40)), 2, 2, 1, thickness=2)
                    cv2.imwrite(os.path.join(debug, (base_name + ".jpg")), img)


if __name__ == "__main__":
    src = "floorplans/fine_tuning"
    debug_imgs(src)


