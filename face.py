import numpy as np
import serial
import time
import sys
import cv2
from playsound import playsound
import threading

from tapTester import TapTester

tt = TapTester()

###########
def play_welcome():
    playsound('audio.mp3')
thr_welcome = threading.Thread(target=play_welcome, args=(), kwargs={})
###########
rps_mode = False
###########

#Setup Communication path for arduino (In place of 'COM5' put the port to which your arduino is connected)
#arduino = serial.Serial('COM3', 9600) 
time.sleep(2)
print("Connected to arduino...")

#importing the Haarcascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#To capture the video stream from webcam.
cap = cv2.VideoCapture(0)

#Read the captured image, convert it to Gray image and find faces
while 1:
    tapped = tt.listen()
    if tapped == True:
        print("Tapped")
        rps_mode = True
    ret, img = cap.read()
    cv2.resizeWindow('img', 500, 500)
    # cv2.namedWindow("img", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("img",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    # cv2.setWindowProperty("img",1,0)
    # cv2.line(img,(500,250),(0,250),(0,255,0),1)
    # cv2.line(img,(250,0),(250,500),(0,255,0),1)
    # cv2.circle(img, (250, 250), 5, (255, 255, 255), -1)
    gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3)

# notes:
# in loop, set booleans. then run functions after img.show
    #####################
    # print(type(faces),faces, isinstance(faces, tuple))
    if not isinstance(faces, tuple):
        for (x,y,w,h) in faces:
            if w < 70 and h < 70:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),5)
            else:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),5)
                # print("WAVE")
                if not thr_welcome.is_alive():
                    thr_welcome = threading.Thread(target=play_welcome, args=(), kwargs={})
                    thr_welcome.start()

# #detect the face and make a rectangle around it.
#     for (x,y,w,h) in faces:
#         cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),5)
#         roi_gray  = gray[y:y+h, x:x+w]
#         roi_color = img[y:y+h, x:x+w]

#         arr = {y:y+h, x:x+w}
#         print (arr)

#         print ('X :' +str(x))
#         print ('Y :'+str(y))
#         print ('x+w :' +str(x+w))
#         print ('y+h :' +str(y+h))

# # Center of roi (Rectangle)
#         xx = int(x+(x+h))/2
#         yy = int(y+(y+w))/2
#         print (xx)
#         print (yy)
#         center = (xx,yy)

# # sending data to arduino
#         print("Center of Rectangle is :", center)
#         data = "X{0:d}Y{1:d}Z".format(xx, yy)
#         print ("output = '" +data+ "'")
#         #arduino.write(data)

#Display the stream.
    cv2.imshow('img',img)

#Hit 'Esc' to terminate execution 
    k = cv2.waitKey(30) & 0xff
    if k == 27:
       break
