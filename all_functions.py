import cv2
import numpy as np

class all_func():
    def __init__(self):
        pass
    def stack_images(self, img_array, ori_img):
        # images_stacked = cv2.hconcat(img_array)
        # cv2.imshow("All images",images_stacked)
        imstack = cv2.resize(ori_img,(500,500))
        
        for img in img_array:
            print(img.shape)
            print(type(img))
            im = cv2.resize(img,(500,500))
            print(im.shape)
            imstack = np.hstack((imstack, im))

        return imstack