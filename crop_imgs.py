import cv2
import os


def crop_imgs(imgs,src, dest):
    for img in os.listdir(src):
        if img.endswith(".jpg") or img.endswith(".png"):
            base_name = os.path.splitext(os.path.basename(img))[0]
            txt = os.path.join(src, (base_name + ".txt"))
            print(base_name) # ex: 001
            print(img) # ex: 001.jpg
            img = cv2.imread(os.path.join(imgs, img))
            #cv2.imshow("image",img)
            with open(txt) as t:
                content = t.readlines()
                i = 1
                crops_dest = os.path.join(dest, (base_name))
                if not os.path.isdir(crops_dest):
                    os.mkdir(crops_dest)
                with open(os.path.join(crops_dest, "crops.txt"), "w") as tc:
                    for box in content:
                        print(box)
                        crop = img[int(box.split(",")[1]):int(box.split(",")[3]), int(box.split(",")[0]):int(box.split(",")[2])]
                        #cv2.imshow("cropped", crop)
                        #cv2.waitKey(0)
                        #cv2.destroyAllWindows()
                        name = 'crop' + str(i)
                        print(name)
                        cv2.imwrite(os.path.join(crops_dest, (name + ".jpg")), crop)
                        tc.write((name + " " + box))
                        i += 1