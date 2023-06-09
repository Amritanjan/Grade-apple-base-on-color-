import cv2 
import numpy as np
cap = cv2.VideoCapture("/home/amritanjan/Downloads/backup/apple vidio/apple.mp4")

# Object detection from Stable camera
#object_detector = cv2.createBackgroundSubtractorMOG2()

def color_of_apple(mask,img):
    G_list=[]
    R_list=[]
    B,G,R=cv2.split(img)
    pts = np.where(mask == 255)
    G_list.append(G[pts[0], pts[1]])
    R_list.append(R[pts[0], pts[1]])
    
    R_count=0
    G_count=0


    for list in zip(G_list,R_list):
        for item in zip(list[0],list[1]):
            if(item[0]>item[1]):
                G_count+=1
            else:
                R_count+=1
    
    red_per=round(((R_count/(R_count+G_count))*100),2)
    #print("Red % is ",red_per)
    
    if(red_per<70):
        print("its green Apple")
    else:
        print("its red Apple")
    
    return(red_per)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape
    #print(height,width)
    # Extract Region of interest
    roi = frame[250: 316,190: 300]
    cv2.imshow("frame",frame)

    #mask = object_detector.apply(roi)
    #cv2.imshow("mask",mask)
    HSV=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
    h,s,v=cv2.split(HSV)
    #cv2.imshow("h",h)
    #cv2.imshow("s",s)
    #cv2.imshow("v",v)
    (ret, thresh) = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #cv2.imshow("thresh",thresh)
    red_per=color_of_apple(thresh,roi)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 100:
            cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
    
    roi = cv2.putText(roi,str(red_per), (int(10),int(40)), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 1, cv2.LINE_AA, False)
    cv2.imshow("img",roi)
    key=cv2.waitKey(0)
    if key==ord('q'):
        break
