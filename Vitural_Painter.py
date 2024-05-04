import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

background_path = resource_path("Images/bg.png")
background = cv2.imread(background_path)
####################################
drawColor = (255,0,255)
eraserThickness = 50
brushThickness = 10
eraser=False
clean=False
##################################
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)


detector = htm.handDetector(detectionCon=0.85)
xp,yp = 0,0
imgCanvas = np.zeros((720,1280,3), np.uint8)

while True:
    # import img
    success, img = cap.read()
    img = cv2.flip(img,1)
    img[0:125, 0:1280] = background
    
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if(len(lmList)) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()

        if fingers[1] and fingers[2]:
            xp,yp = 0,0
            print("Selection Mode")
            if y1 < 125:
                if 345 < x1 < 430:
                    drawColor = (0, 0, 255)
                elif 430 < x1 < 520:
                    drawColor = (0, 255, 255)
                elif 520 < x1 < 610:
                    drawColor = (255, 0, 0)
                elif 610 < x1 < 695:
                    drawColor = (0, 255, 0)
                elif 695 < x1 < 780:
                    drawColor = (0, 128, 255)
                elif 780 < x1 < 870:
                    drawColor = (255, 0, 255)
                elif 870 < x1 < 960:
                    drawColor = (255, 255, 255)
                elif 960 < x1 < 1045:
                    drawColor=(0,0,0)
                elif 1150 < x1 < 1250:
                    clean=True
            cv2.rectangle(img,(x1,y1-25), (x2, y2+25), drawColor, cv2.FILLED)

        if fingers[1] and fingers[2]==False:
            cv2.circle(img, (x1,y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp==0 and yp==0:
                xp,yp = x1,y1
            if clean == True:
                imgCanvas = np.zeros((720,1280,3), np.uint8)
                clean = False
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp,yp), (x1,y1),(0, 0, 0),eraserThickness)
                cv2.line(imgCanvas, (xp,yp), (x1,y1),(0, 0, 0),eraserThickness)
            else:
                cv2.line(img, (xp,yp), (x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas, (xp,yp), (x1,y1),drawColor,brushThickness)
            
            xp,yp = x1,y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)     
    _, imgInv = cv2.threshold(imgGray, 10,255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img  = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)


    img[0:125, 0:1280] = background
    #img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    
    # Sử dụng kích thước màn hình để hiển thị cửa sổ OpenCV full màn hình
    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow("Image", img)
    cv2.waitKey(1)