import cv2
import time
import os
import handcrackingmodule as hmt

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderpath = "fingerimages"
myList = os.listdir(folderpath)
print(myList)
overlaylist = []
for impath in myList:
    image = cv2.imread(f'{folderpath}/{impath}')
    overlaylist.append(image)

ptime =0
detector = hmt.HandDetector(detectionconf=0.75)

tipids = [4,8,12,16,20]

while True:
    success, img = cap.read()
    img = detector.findhands(img)
    lmList = detector.findPosition(img, draw=False)
    #print(lmList)
    if len(lmList) !=0:
        fingers = []
        #Thump
        if lmList[tipids[0]][1] < lmList[tipids[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #foure fingers
        for id in range(1,5):
            if lmList[tipids[id]][2] < lmList[tipids[id]-3][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalfingers = fingers.count(1)
        print(totalfingers)

        cv2.rectangle(img, (20, 255),(170,425), (0,255), cv2.FILLED)
        cv2.putText(img, str(totalfingers), (45,375), cv2.FONT_HERSHEY_PLAIN, 10, (255,0,0), 25)

    # h, w, c = overlaylist[0].shape
    # img[0:h,0:w] = overlaylist[0]



    ctime = time.time()
    fps =1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, f'FPS: {int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,3, (255,0,0),3)

    cv2.imshow('image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
                break
cap.release()
cv2.destroyAllWindows()
   

