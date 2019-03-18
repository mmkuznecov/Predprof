from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2
import webbrowser
import svgwrite

def draw_svg(shape, color, coordinates):
    if shape=="circle":
        
    elif shape=="half_circle":

    elif shape=="pentagon":

    elif shape=="square":

    elif shape=='rectangle':
    
    else:
        print("Undefined shape")

    return path

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


def detect_shapes(frame):
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


    for c in cnts:
        M = cv2.moments(c)
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

    return [shape,[c]]


if __name__ == "__main__":
    camera = cv2.VideoCapture(1)
    while True:
        (grabbed, frame) = camera.read()
        detect_shapes(frame)
        color_detection(frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            bryaka()
            break