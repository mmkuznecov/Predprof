from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2

'''ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",help="path to the (optional) video file")
ap.add_argument("-b", "--buffer",type=int, default=64,help="max buffer size")
args = vars(ap.parse_args())'''

#if not args.get("video", False):
camera = cv2.VideoCapture(1)
#else:
#    camera = v2.VideoCapture(args["video"])

while True:
    (grabbed, frame) = camera.read()

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
            key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
camera.release()
cv2.destroyAllWindows()
