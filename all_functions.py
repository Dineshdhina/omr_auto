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

    def rectangle_contour(self,contours):
        rect_cont = []
        for contour in contours:
            area = cv2.contourArea(contour)   
            if area > 50:
                peri = cv2.arcLength(contour, True)
                print(peri)
                approx = cv2.approxPolyDP(contour, 0.02*peri,True)
                if len(approx) == 4:
                    rect_cont.append(contour)

                
            
