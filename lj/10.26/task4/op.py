'''
Author: linin00
Date: 2022-10-26 18:41:23
LastEditTime: 2022-11-01 22:23:29
LastEditors: linin00
Description: 
FilePath: /lj/10.26/task4/op.py

'''
import numpy as np
import cv2
from MXMqtt import MXMqtt
face_model = 'model/haarcascade_frontalface_default.xml'
eye_model  = 'model/haarcascade_eye.xml'
face_cascade = cv2.CascadeClassifier(face_model)
eye_cascade  = cv2.CascadeClassifier(eye_model)

LEFT = 1
RIGHT = 2
FORWARD = 3
BACKWARD = 4
STANDBY = 5
NOFACE = 0

left_i = cv2.imread("img/left.png")
right_i = cv2.imread("img/right.png")
backward_i = cv2.imread("img/backward.png")
forward_i = cv2.imread("img/forward.png")
standby_i = cv2.imread("img/standby.png")
noface_i = cv2.imread("img/noface.png")
mqtt = MXMqtt("mqtt.16302.com", 1883)

def reprint(img, dir, x, y):
  text = "error"
  tmp = noface_i
  if dir == LEFT:
    text = "left"
    tmp = left_i
  elif dir == RIGHT:
    text = "right"
    tmp = right_i
  elif dir == FORWARD:
    text = "forward"
    tmp = forward_i
  elif dir == BACKWARD:
    text = "backward"
    tmp = backward_i
  elif dir == STANDBY:
    text = "standby"
    tmp = standby_i
  elif dir == NOFACE:
    return
  cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)
  w = img.shape[1]
  h = img.shape[0]
  b_x = w - 50
  e_x = w
  b_y = h - 50
  e_y = h
  img[h-50:h, w-50:w]=tmp

def face2direction(img) :
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  width = img.shape[1]
  hight = img.shape[0]
  print(gray.shape)
  if (len(faces) == 1) :
    for (x, y, w, h) in faces:
      img = cv2.rectangle(img,(x, y), (x+w, y+h), (255, 0, 0), 2)
      mid = x + w/2
      if mid < width/3 :
        mqtt.PUB("LJ", "LEFT")
        reprint(img, LEFT, x, y)
        return img, LEFT
      elif mid > 2*width/3 :
        mqtt.PUB("LJ", "RIGHT")
        reprint(img, RIGHT, x, y)
        return img, RIGHT
      elif w > width/3 :
        mqtt.PUB("LJ", "TOP")
        reprint(img, FORWARD, x, y)
        return img, FORWARD
      elif w < width/5 :
        mqtt.PUB("LJ", "DOWN")
        reprint(img, BACKWARD, x, y)
        return img, BACKWARD
      else :
        mqtt.PUB("LJ", "STAND_BY")
        reprint(img, STANDBY, x, y)
        return img, STANDBY

  return img, NOFACE

def handleDir(img, dir) :
  if dir == NOFACE:
    print("no face in th screen\t👻")
  elif dir == LEFT :
    print("left\t👈")
  elif dir == RIGHT :
    print("right\t👉")
  elif dir == FORWARD :
    print("forward\t🫵")
  elif dir == STANDBY :
    print("standby\t🖐")
  elif dir ==BACKWARD :
    print("backward\t🤌")
  else :
    print("something wrong")

if __name__ == "__main__":
  cap = cv2.VideoCapture(0)
  while(True):
    ret, frame = cap.read()
    img = cv2.flip(frame, 1)
    img, dir = face2direction(img)
    handleDir(img, dir)
    cv2.imshow('frame', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  cap.release()
  cv2.destroyAllWindows()
