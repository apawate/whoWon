import numpy as np
import cv2 as cv

race = input("Enter the video file name: ")
cap = cv.VideoCapture(race)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
