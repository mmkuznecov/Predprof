from pyimagesearch.shapedetector import ShapeDetector
import argparse
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

def pentagonCoords(side):
    coords = []
    angle = -72
    for i in range(5):
        angle += 72
        radian_angle = math.radians(angle)
        x = side * math.sin(radian_angle) + 100
        y = side * math.cos(radian_angle) + 100
        coord = (x, y)
        coords.append(coord)
    return coords

def draw_svg(code, color='black'):
    dwg = svgwrite.Drawing(filename='svg_image.svg', debug=True)

    if code == "R":
        dwg.add(dwg.rect(insert=(1*cm, 1*cm), size=(40*mm, 20*mm),
                        fill=color, stroke='black', stroke_width=3))
    elif code == "S":
        dwg.add(dwg.rect(insert=(1*cm, 1*cm), size =(28*mm, 28*mm), fill = color, stroke = 'black', stroke_width = 3 ))
 
    elif code == "P":
        dwg.add(dwg.polygon(points = pentagonCoords(float(100)), fill = color, stroke = 'black', stroke_width = 3))

    elif code == "H":
        dwg.add(dwg.circle(center=(2*cm, 2*cm), r='17.5mm', stroke='black', fill=color,
                          stroke_width=3))
        dwg.add(dwg.rect(insert=(0*cm, 2*cm), size=(40*mm, 40*mm),
                        fill='white', stroke='black', stroke_width=0))
        dwg.add(dwg.line(start=(0.25*cm, 2*cm ), end=(3.75*cm, 2*cm), stroke = 'black', stroke_width = 3))

    elif code == "C":
        dwg.add(dwg.circle(center=(2*cm, 2*cm), r='17.5mm', stroke='black', stroke_width=3, fill=color))

    # code = "L"
    dwg.save()

def send_signal(port,sig):
    port.write(sig)

def steps(port):
    ser = serial.Serial("/dev/ttyACM0",9600,timeout=5)
    ser.write('D') #move for a few steps


def open_brows(path_to_image):
    browser = webbrowser.get("google-chrome")
    browser.open(path_to_image)

def color_detection(frame):
    lower = {'red':(166, 84, 141), 'green':(66, 122, 129), 'blue':(97, 100, 117), 'yellow':(23, 59, 119), 'orange':(0, 50, 80)}
    upper = {'red':(186,255,255), 'green':(86,255,255), 'blue':(117,255,255), 'yellow':(54,255,255), 'orange':(20,255,255)}
    colors = {'red':(0,0,255), 'green':(0,255,0), 'blue':(255,0,0), 'yellow':(0, 255, 217), 'orange':(0,140,255)}
    
    frame = imutils.resize(frame, width=600)
 
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    for key, value in upper.items():
       
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
               
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
       
        if len(cnts) > 0:
            
            return key


    
def bryaka():
    camera.release()
    cv2.destroyAllWindows()


def proverkaNaTocecki(tocecka, height_edge, width_edge):
  for tod in tocecka:
      # print("aaaa", tod[0])
      tdx = tod[0][0]
      tdy = tod[0][1]
      if tdx in width_edge or tdy in height_edge:
          print('On the edge')
          return False

  # print('AAAA', tocecka_x, tocecka_y)
  return True

def detect_shapes(frame):
    usl = True
    frame = imutils.rotate(frame, angle=180)
    resized = imutils.resize(frame, width=300)
    ratio = frame.shape[0] / float(resized.shape[0])

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()
    height, width = frame.shape[:2]
    width_edge = list(range(0, 11)) + list(range(width - 10, width + 1))
    height_edge = list(range(0, 11)) + list(range(height - 10, height + 1))
    if len(cnts)==0:
        usl=True
    elif len(cnts) == 1:
        for c in cnts:
            if not proverkaNaTocecki(c, height_edge, width_edge):
                continue
            else:
                usl=False
            M = cv2.moments(c)
            print(c)
            if(M["m00"]==0): # this is a line
                shape = "line" 
            else: 
                cX = int((M["m10"] / M["m00"]) * ratio)
                cY = int((M["m01"] / M["m00"]) * ratio)
                shape = sd.detect(c)

                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
                cv2.putText(frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 0), 2)

                cv2.imshow("Gambar", frame)
                if usl==False:

                    if shape == 'rectangle':
                        code = "R"
                    elif shape == 'square':
                        code = "S"
                    elif shape == 'pentagon':
                        code = "P"
                    elif shape == 'semicircle':
                        code = "H"
                    elif shape == 'circle':
                        code = "C"
                    else:
                        code = "L"
                    
                    draw_svg(code)

            try:
                return code 
            except Exception:
                return None


if __name__ == "__main__":
    ser = serial.Serial("/dev/ttyACM0",9600,timeout=5) #define as global?
    camera = cv2.VideoCapture(1)
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            bryaka()
            break
        (grabbed, frame) = camera.read()
        try:
            a = detect_shapes(frame)
            # b = color_detection(frame)
            if a is not None:
                send_signal(a) # realise motor moving function
            else:
                continue
        except Excpetion as e:
            print(e)
            bryaka()
        #color_detection(frame)
        
        



'''import serial
import time
ser = serial.Serial("/dev/ttyACM0",9600,timeout=5)
while True:
    ser.write('A')

    time.sleep(2)'''
