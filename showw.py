from imutils.video import VideoStream
from tkinter import *
import argparse
import datetime
import imutils
import time
import cv2

def showe():
    vs = cv2.VideoCapture("sample.mp4")

    img = cv2.imread("frame673.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (21, 21), 0)

    firstFrame = None

    while True:
            frame = vs.read()
            frame = frame[1]
            text = "Unoccupied"
     
            if frame is None:
                    break
                
            live = imutils.resize(frame, width=350)
            frame = imutils.resize(frame, width=1376)
            frame = frame[535:1032,0:1376]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
     
            if firstFrame is None:
                    firstFrame = img
                    continue
                
            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
     
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            
            for c in cnts:
                    if cv2.contourArea(c) < 40000 or cv2.contourArea(c) > 100000 :
                            continue
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    text = "Occupied"
            
            cv2.putText(live, "Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(live, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            cv2.namedWindow("Frame")        
            cv2.moveWindow("Frame",50,290)
            cv2.imshow("Frame", frame)
            cv2.imshow("Security Feed", live)
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord("q"):
                    break

    vs.release()
    cv2.destroyAllWindows()
