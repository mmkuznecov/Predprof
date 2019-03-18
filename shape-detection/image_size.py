import cv2
import numpy 
img = cv2.imread('shapes_and_colors.png',0)
height, width = img.shape[:2]
print('Height: ',height)
print('Width: ',width)