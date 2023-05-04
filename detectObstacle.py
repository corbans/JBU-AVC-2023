# import libraries
import cv2
import math as mt
import serial
from picamera import PiCamera
from picamera.array import PiRGBArray

# set up camera tools using libcamera (legacy not permitted in Raspberry Pi)
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 35
rawCapture = PiRGBArray(camera,size=(640,480))

# define color ranges
BLUE_LOWER = (98, 96, 80) # BLUE
BLUE_UPPER = (131, 255, 93) # BLUE
RED_LOWER = (135, 164, 17) # RED
RED_UPPER = (176, 255, 255) # RED
YELLOW_LOWER = (0, 83, 89) # YELLOW
YELLOW_UPPER = (86, 220, 255) # YELLOW

# colors global value
BLUE = [BLUE_LOWER,BLUE_UPPER]
RED = [RED_LOWER,RED_UPPER]
YELLOW = [YELLOW_LOWER,YELLOW_UPPER]
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

try: #initiate serial connection
  arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
  if arduino.isOpen():
    print("{} connected!".format(arduino.port))
except:
  print("ERROR - Could not open serial port")
  exit()


def find_bucket(frame,color):
  hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
  hsv=cv2.GaussianBlur(hsv, (5,5), cv2.BORDER_DEFAULT)
  mask=cv2.inRange(hsv,color[0],color[1])
  _,mask1=cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
  cnts,_=cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
  for c in cnts:
    x = 300
    if cv2.contourArea(c)>x:
      x,y,w,h=cv2.boundingRect(c)  
      cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
      M = cv2.moments(c)
      if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        if cx not in range((mt.floor(W/2) - 55), (mt.floor(W/2) + 56)):   # if object not centered
          if cx in range(0, (mt.floor(W/2) - 55)): # if in left side of frame
              cmd="L"
              print(cmd)
              arduino.write(cmd.encode())
          else:                                   # if in right side of frame
              cmd="R"
              print(cmd)
              arduino.write(cmd.encode())
        else:                             # if condition above is not true, object is centered
          cmd="C"
          print(cmd)
          arduino.write(cmd.encode())
    

while True:
  for img in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    FRAME = img.array
    H,W=FRAME.shape[:2]
    find_bucket(FRAME, YELLOW)
    find_bucket(FRAME, BLUE)
    rawCapture.truncate(0)
    if cv2.waitKey(1)&0xFF==ord('y'):
        cv2.destroyAllWindows()
        break

