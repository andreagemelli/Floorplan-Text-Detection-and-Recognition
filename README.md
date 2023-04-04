## DDM Project ##

This code is able to detect and recognize text inside floorplans. 
We used two different networks to achieve this purpose (add these projects cloning from their repo):

+ txt_det, a ctpn (connectionist text proposal network) that can be found 
[here](https://github.com/eragonruan/text-detection-ctpn)
* txt_recognition, a Convolutional Recurrent Neural Network (CRNN) in pytorch, and its code can be found
[here](https://github.com/meijieru/crnn.pytorch)

All the details of this works can be found in our <a href="https://drive.google.com/file/d/18L63UVQBivzCFA9xcP_imn7Hd6HP1Tws/view?usp=share_link">report</a>.<br>
For data and model checkpoints directly write to me.

***

## Dependencies ##
* Python 3.5.4
* Tensorflow 1.8.0
* PyTorch 0.4.0
* Cuda V9.1.85
* Cudnn 7.1
* Cv2 3.4.1

***

## Prepare Training Data ##
To prepare data for training:

1. First of all, change the paths of images and their labels inside the files of the folder prepare_training;
2. then, run these commands:

    `python prepare_training/jsonAll.py`  
	`python prepare_training/run_split_label.py`  
	`python prepare_training/run_toVoc.py`

You will find a new folder inside floorplans with name 'training'.
If you want to do data augmentation before prepare  
your training data, just run:
`python data_augmentation.py`
and then remember to change paths as before.

## Train and test ##
Before run train, change paths inside`txt_det/ctpn/text.yml` and `txt_det/lib/fast_crnn/config.py`.
Then just run train with `python prepare_training/run_train.py`
For test, use script `evaluate.py`

## Fine Tuning ##
If you want to fine tune the network, follow this steps. Rememeber that
you can find the weights of the first model in the folder called
"checkpoints/pretrained".

* copy the folder pretrained in a new one "fine_tuning"
* change this path inside `prepare_training/run_train.py`
* change the variable `restore` inside `text.yml` and `config.py`, from 0 to 1
* modify `/txt_det/lib/fast_rcnn/train.py` in:
	* line 107: `tvars = tf.trainable_variables()[-2:]`
	* line 133: `#restore_iter = int(stem.split('_')[-1])`

## Try Full Project ##
To run a complete version of the code, run `python main.py [arg]`, where [arg] can be:

* det: for detection
* crop: to crop the bounding boxes of all floorplans
* rec: to recognize text inside all the bounding boxes

To see what's happened, just run `python debug_imgs.py`
