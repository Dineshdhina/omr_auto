import cv2 
import numpy as np
import sys
sys.path.append(".")
from all_functions import all_func


width = 500
height = 500


img = cv2.imread("1.jpg")
imgcontours = img.copy()

imgs = cv2.resize(img,(width,height))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5,5),1)
imgCanny = cv2.Canny(imgBlur, 10, 50)

contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgcontours, contours, -1, (0,255,0), 10)
image_contours = cv2.resize(imgcontours,(width,height))


image_array =[imgBlur, imgCanny]

funcs = all_func()
imstack = funcs.stack_images(image_array,imgGray)

cv2.imshow("Original",imstack)
cv2.imshow("contours",image_contours)
cv2.waitKey(0)