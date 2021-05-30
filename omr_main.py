import cv2 
import numpy as np
import sys
sys.path.append(".")
from all_functions import all_func


width = 700
height = 700
questions = 5
choices = 5
answers = [1,2,0,1,4]
funcs = all_func()

img = cv2.imread("1.jpg")
imgcontours = img.copy()

bigimgcontours = img.copy()
# preprocess the images
imgs = cv2.resize(img,(width,height))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5,5),1)
imgCanny = cv2.Canny(imgBlur, 10, 50)
img_Final = imgs.copy()
# find all contours
contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgcontours, contours,-1, (0,255,0), 10)
image_contours = cv2.resize(imgcontours,(width,height))


# find rectangles
rect_cont = funcs.rectangle_contour(contours)
big_contour = funcs.getCornerPoints(rect_cont[0])
gradePoints = funcs.getCornerPoints(rect_cont[1])


# find perspective and wrap the images
if big_contour.size != 0 and gradePoints.size !=0:
    cv2.drawContours(bigimgcontours,big_contour, -1,(0,255,0),40)
    cv2.drawContours(bigimgcontours,gradePoints, -1,(0,255,0),40)

    biggest_contour = funcs.reorder(big_contour)
    gradePoints = funcs.reorder(gradePoints)

    pt1 = np.float32(biggest_contour)
    pt2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
    matrix = cv2.getPerspectiveTransform(pt1,pt2)
    imgwrapColored = cv2.warpPerspective(img,matrix,(width,height))
  
    pt1_g = np.float32(gradePoints)
    pt2_g = np.float32([[0,0],[300,0],[0,150],[300,150]])
    matrix_g = cv2.getPerspectiveTransform(pt1_g,pt2_g)
    imgwrapColored_g = cv2.warpPerspective(img,matrix_g,(300,150))

    # find the bubbles which are marked by applying the threshold
    img_wrap_gray = cv2.cvtColor(imgwrapColored, cv2.COLOR_BGR2GRAY)
    imgThrash = cv2.threshold(img_wrap_gray, 150,225, cv2.THRESH_BINARY_INV)[1] # if the pixel value is smaller than the threshold, it is set to 0

    boxes = funcs.split_boxes(imgThrash)
    cv2.imshow("test", boxes[2])

    # getting the nonzero pixel values
    mypixelvalues = np.zeros((questions,choices))
    countR = 0
    countC = 0
    for image in boxes:
        totalPixels = cv2.countNonZero(image)
        mypixelvalues[countR][countC] = totalPixels
        countC +=1
        if (countC == choices):countR +=1 ;countC= 0
    
    # finding index values of the markings
    myinndex = []
    for x in range(0,questions):
        arr = mypixelvalues[x]
        print("arr", arr)
        myIndexval = np.where(arr == np.amax(arr))
        myinndex.append(myIndexval[0][0])
    
    grading = []
    for x in range(0,questions):
        if answers[x] == myinndex[x]:
            grading.append(1)
        else:
            grading.append(0)
        
    score = (sum(grading)/questions) * 100 
    print(score)
    
 
    #display answers
    image_results = imgwrapColored.copy()
    result_image = funcs.showAnserws(image_results,myinndex,grading,answers,questions,choices)
    imRawDrawing = np.zeros_like(imgwrapColored)
    imRawDrawing = funcs.showAnserws(imRawDrawing,myinndex,grading,answers,questions,choices)
    print("imgDrawing: ",imRawDrawing.shape)
    invMatrix = cv2.getPerspectiveTransform(pt2,pt1)
    imgInvwarp = cv2.warpPerspective(imRawDrawing, invMatrix,(width,height))
    funcs.shift_image(imgInvwarp,40)
    print("image_final:",img_Final.shape)
    print("imgWrap:",imgInvwarp.shape)


    imgRawGrade = np.zeros_like(imgwrapColored_g)
    cv2.putText(imgRawGrade, str(int(score))+"%",(60,100),cv2.FONT_HERSHEY_COMPLEX,3,(0,255,255),3)
    cv2.imshow("Grade",imgRawGrade)
    inv_matrix_g = cv2.getPerspectiveTransform(pt2_g,pt1_g)
    inv_imgwrapColored_g = cv2.warpPerspective(imgRawGrade,inv_matrix_g,(width,height))
    img_Final = cv2.addWeighted(img_Final,1,imgInvwarp,1.5,0)
    img_Final = cv2.addWeighted(img_Final,1,inv_imgwrapColored_g,1.5,0)








image_array =[imgBlur,imgThrash]
image_array_3d = [image_contours,bigimgcontours,imgwrapColored,imgwrapColored_g]
result_colored = [result_image,imgInvwarp]

imstack = funcs.stack_images(image_array,imgGray,2)
imstack_3d = funcs.stack_images(image_array_3d,img,3)
imstack_result_coloured = funcs.stack_images(result_colored,img,3)

# cv2.imshow("Original",imstack)
# cv2.imshow("contours",imstack_3d)
# cv2.imshow("result",imstack_result_coloured)
# cv2.imshow("inversed",img_Final)
# plotting images using matplotlib
# for i in range(6):
#     plt.subplot(2,3,i+1),plt.imshow(images[i],'gray',vmin=0,vmax=255)
#     plt.title(titles[i])
#     plt.xticks([]),plt.yticks([])
# plt.show()
cv2.waitKey(0)