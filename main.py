import numpy as np
import cv2 as cv

race = input("Enter the video file name: ")
width = int(input("How many seconds should the finish cover? "))
width = width * 30
col = width
cap = cv.VideoCapture(race)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    #cv.imshow('frame', frame)
    height = frame.shape[0]
    if col == width:
        output = np.zeros((height, width, 3), np.uint8)
    snippet = frame[0:height-1, 0:1]
    output[0:height-1, col-1:col] = snippet
    cv.imshow('who won?', output)
    col = col - 1
    if cv.waitKey(1) == ord('q'):
        break

cv.imwrite("finish.png", output)
cap.release()
cv.destroyAllWindows()
