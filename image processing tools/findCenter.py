import cv2
import numpy as np
import math as mt
from picamera import PiCamera
from picamera.array import PiRGBArray

camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera,size=(640,480))

BLUE_LOWER = (110, 130, 15) # BLUE
BLUE_UPPER = (139, 255, 255) # BLUE
RED_LOWER = (135, 164, 17) # RED
RED_UPPER = (176, 255, 255) # RED
YELLOW_LOWER = (11, 164, 54) # YELLOW
YELLOW_UPPER = (105, 255, 255) # YELLOW
WOOD_LOWER = (12,3,193) #RAMP
WOOD_UPPER = (93, 93, 255) #RAMP
# colors global value
BLUE = [BLUE_LOWER,BLUE_UPPER]
RED = [RED_LOWER,RED_UPPER]
YELLOW = [YELLOW_LOWER,YELLOW_UPPER]
RAMP = [WOOD_LOWER,WOOD_UPPER]
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def find_bucket(frame):
  hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
  hsv=cv2.GaussianBlur(hsv, (5,5), cv2.BORDER_DEFAULT)
  mask=cv2.inRange(hsv,YELLOW[0], YELLOW[1])
  _,mask1=cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
  cnts,_=cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
  for c in cnts:
    x = 300
    if cv2.contourArea(c)>x:
      x,y,w,h=cv2.boundingRect(c)  
      cv2.circle(frame, (x,y), 2, (0,255,0), -1)
      cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
      M = cv2.moments(c)
      if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.circle(frame, (cx,cy), 2, (0,255,0), -1)
        cv2.putText(frame, f"cx: {cx}", (cx, cy),cv2.FONT_HERSHEY_COMPLEX, 0.6, (GREEN), 2)
        cv2.putText(frame, f"count: {len(M)}", (65, 35),cv2.FONT_HERSHEY_COMPLEX, 0.6, (GREEN), 2)
        if cx not in range((mt.floor(W/2) - 50), (mt.floor(W/2) + 51)):   # if object not centered 
          if cx in range(0, (mt.floor(W/2) - 50)): #left
            cmd="L"
          else: #right
            cmd="R"
        else:
          cmd="C"

for img in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = img.array
    H,W=frame.shape[:2]
    find_bucket(frame)
    cv2.imshow("FRAME",frame)
    rawCapture.truncate(0)
    if cv2.waitKey(1)&0xFF==ord('y'):
        cv2.imwrite('img_processing/notcentered.jpg', frame)
        cv2.destroyAllWindows()
        break