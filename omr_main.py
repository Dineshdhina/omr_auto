import cv2 
import numpy as np
import sys
sys.path.append(".")
from all_functions import all_func


width = 500
height = 500
funcs = all_func()

img = cv2.imread("1.jpg")
imgcontours = img.copy()
bigimgcontours = img.copy()
# preprocess the images
imgs = cv2.resize(img,(width,height))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5,5),1)
imgCanny = cv2.Canny(imgBlur, 10, 50)

# find all contours
contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgcontours, contours,-1, (0,255,0), 10)
image_contours = cv2.resize(imgcontours,(width,height))


# find rectangles
rect_cont = funcs.rectangle_contour(contours)
big_contour = funcs.getCornerPoints(rect_cont[0])
gradePoints = funcs.getCornerPoints(rect_cont[1])



if big_contour.size != 0 and gradePoints.size !=0:
    cv2.drawContours(bigimgcontours,big_contour, -1,(0,255,0),40)
    cv2.drawContours(bigimgcontours,gradePoints, -1,(0,255,0),40)

    biggest_contour = funcs.reorder(big_contour)
    gradePoints = funcs.reorder(gradePoints)


image_array =[imgBlur, imgCanny]
image_array_3d = [image_contours,bigimgcontours]

imstack = funcs.stack_images(image_array,imgGray,2)
imstack_3d = funcs.stack_images(image_array_3d,img,3)


cv2.imshow("Original",imstack)
cv2.imshow("contours",imstack_3d)
cv2.waitKey(0)