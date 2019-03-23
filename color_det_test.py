from pyimagesearch.shapedetector import ShapeDetector
import imutils
import cv2
import webbrowser
import numpy as np
import serial
import time
from datetime import datetime
import svgwrite
import os 
from svgwrite import cm, mm
import math

def color_detection(frame):
    #print('jopa')
    cv2.imshow('a',frame)
    lower = {'white': (254,254,254),'brown': (99,61,40)}
    upper = {'white': (255,255,255),'brown': (150,120,105)}
    #colors = {'red':(0,0,255), 'green':(0,255,0), 'blue':(255,0,0), 'yellow':(0, 255, 217), 'orange':(0,140,255)}
    signals = {'brown':'B','white':"W"}
    
    frame = imutils.resize(frame, width=600)
 
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    #print('jojo')

    for key, value in upper.items():
       
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        cv2.imshow('Maskr',mask)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        cv2.imshow('Mask',mask)
               
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        #print('jjba')
       
        if len(cnts) > 0:
            return signals[key]
            #print(signals[key])
            

if __name__ == "__main__":
    try:
        ser = serial.Serial("/dev/ttyACM0",9600,timeout=5) #define as global?
    except Exception as e:
        print("Can't connect to port")
    #key = cv2.waitKey(0) & 0xFF
    cam = cv2.VideoCapture(1)
    #color_detection(frame)
    #time.sleep(5)
    while True:
        #print('img grabbed')
        (grabbed, frame) = cam.read()
        a = color_detection(frame)
        print(a)
        if a != None:
            try:
                send_signal(ser,a)
            except Exception as e:
                print("Cannot send a signal")
        else:
            try:
                steps()
            except Exception as e:
                print("Cannot send a signal")
        #print(a)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            #bryaka()
            break
    cam.release()
    cv2.destroyAllWindows()