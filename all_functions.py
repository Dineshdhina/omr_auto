import cv2
import numpy as np

class all_func():
    def __init__(self):
        pass
    def stack_images(self, img_array, ori_img, dim):
        # images_stacked = cv2.hconcat(img_array)
        # cv2.imshow("All images",images_stacked)
        if dim == 3:
            imstack = cv2.resize(ori_img,(700,700))
        
            for img in img_array:
                print(img.shape)
                print(type(img))
                im = cv2.resize(img,(700,700))
                print(im.shape)
                imstack = np.hstack((imstack, im))
            return imstack
        else:
            imstack = cv2.resize(ori_img,(700,700))
        
            for img in img_array:
                print(img.shape)
                print(type(img))
                im = cv2.resize(img,(700,700))
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

    def split_boxes(self, image):
        rows = np.vsplit(image,5)
        boxes = []
        for row in rows:
            cols = np.hsplit(row, 5)
            for box in cols:
                boxes.append(box)
        return boxes


    def showAnserws(self,img,myindex,grading,ans, questions, choices):
        sectionWidth = int(img.shape[1]/questions)
        sectionHeight = int(img.shape[0]/choices)

        for x in range(0, questions):
            myanswer = myindex[x]
            #TODO
            centerX = (myanswer*sectionWidth) + sectionWidth//2
            centerY = (x*sectionHeight) +sectionHeight//2

            if grading[x] ==1:
                mycolor = (0,255,0)
            else:
                mycolor = (0,0,255)
                correctAns = ans[x]
                CX = (correctAns*sectionWidth) + sectionWidth//2
                CY = (x*sectionHeight) +sectionHeight//2
                cv2.circle(img,(CX,CY),25,(0,255,0),cv2.FILLED)

            cv2.circle(img,(centerX,centerY),25,mycolor,cv2.FILLED)

        return img
                
            
    def shift_image(self,image,shift):
        # for i in range(image.shape[1] -1, image.shape[1] - shift, -1):
        #     image = np.roll(image, -1, axis=1)
        #     image[:, -1] = 0
        h, w, c = image.shape 
         #set shift magnitude
        img_shift_right = np.zeros(image.shape)
        img_shift_down = np.zeros(image.shape)
        img_shift_left = np.zeros(image.shape)
        img_shift_up = np.zeros(image.shape)



        img_shift_right[:,shift:w, :] = image[:,:w-shift, :]
        img_shift_down[shift:h, :, :] = image[:h-shift, :, :]
        img_shift_left[:,:w-shift, :] = image[:,shift:, :]
        img_shift_up[:h-shift, :, :] = image[shift:, :, :]
        cv2.imshow('left shifted image', img_shift_left)
        cv2.imshow('right shifted image', img_shift_right)
        cv2.imshow("Up shifted image",img_shift_up)

        cv2.waitKey()

    
