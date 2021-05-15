import cv2
import numpy as np

class all_func():
    def __init__(self):
        pass
    def stack_images(self, img_array, ori_img, dim):
        # images_stacked = cv2.hconcat(img_array)
        # cv2.imshow("All images",images_stacked)
        if dim == 3:
            imstack = cv2.resize(ori_img,(500,500))
        
            for img in img_array:
                print(img.shape)
                print(type(img))
                im = cv2.resize(img,(500,500))
                print(im.shape)
                imstack = np.hstack((imstack, im))
            return imstack
        else:
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
                approx = cv2.approxPolyDP(contour, 0.02*peri,True)
                if len(approx) == 4:
                    rect_cont.append(contour)

        rect_cont = sorted(rect_cont, key = cv2.contourArea , reverse = True)

        return rect_cont

    def getCornerPoints(self, cont):
        peri = cv2.arcLength(cont, True)
        approx = cv2.approxPolyDP(cont, 0.02*peri,True)
        return approx

    def reorder(self, points):
        points = points.reshape((4,2))
        pointsnew = np.zeros((4,1,2),np.int32)
        add = points.sum(1)
        pointsnew[0] = points[np.argmin(add)] 
        pointsnew[3] = points[np.argmax(add)] 
        diff = np.diff(points,axis = 1)
        pointsnew[1] = points[np.argmin(diff)]
        pointsnew[2] = points[np.argmax(diff)]

        return pointsnew



                
            
