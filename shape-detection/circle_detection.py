import cv2 
import numpy as np
from math import pi, cos, sin

color = cv2.imread('circles.png')
#color = cv2.medianBlur(color,5)

cv2.imshow('Orig',color)

gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)

canny = cv2.Canny(gray,200,20)
#print(cv2.HOUGH_GRADIENT)
#print(gray)
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 60, param1=200, param2=20, minRadius=0, maxRadius=0)
#circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
print(circles)
circles = np.uint16(np.around(circles))
print(circles)
for i in circles[0,:]:
    cv2.circle(color,(i[0],i[1]),i[2],(0,255,0),1)
    # draw the center of the circle
    cv2.circle(color,(i[0],i[1]),2,(0,0,255),-1)

cv2.imshow('Circles',color)


#dt = cv2.distanceTransform(255, cv2.DIST_L2 ,3)
dt= cv2.distanceTransform(255-canny,cv2.DIST_L2,3) 

cv2.imshow('Hu',dt)
#cv2.waitKey(0)

print(dt)
print(len(dt))
print(len(dt[0]))
print(len(dt[1]))
minInlierDist = 2.0


for i in circles[0,:]:
    print(i[0])
    print(i[1])
    counter = 0
    inlier = 0
    maxInlierDist = i[2]/25
    #print("Radius_b: ", i[2])
    #print(maxInlierDist)
    
    if maxInlierDist<minInlierDist:
        maxInlierDist = minInlierDist

    t=0
    while t<2*pi:
        
        counter+=1
        cX = i[2]*cos(t) #+ i[0]
        cY = i[2]*sin(t) #+ i[1]
        #print(cX)
        #print(cY)
        if dt[int(cY)][int(cX)] < maxInlierDist:
            inlier+=1
            cv2.circle(color,(int(cX),int(cY)),3, (0,255,0))
        else:
            cv2.circle(color,(int(cX),int(cY)),3, (255,0,0))
        t+=0.1

    print(100*int(inlier)/int(counter)," rad ", i[2])

cv2.imshow('output',color)


cv2.waitKey(0)
















'''
#img = cv.medianBlur(img,5)
cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=0,maxRadius=0)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
cv.imshow('detected circles',cimg)
cv.waitKey(0)
cv.destroyAllWindows()'''