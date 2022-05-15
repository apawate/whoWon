import numpy as np
import cv2 as cv

race = input("Enter the video file name: ")
step = float(input("How often should timestamps be in seconds? "))
step = step * 30
step = int(step)
cap = cv.VideoCapture(race)
width = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
col = width

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
black = np.zeros((height, 1, 3), np.uint8)
for x in range(width-1, 0, -step):
    output[0:height, x-1:x] = black
    output = cv.putText(output, str(x/30), (int(x * step), height-1), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0))

cv.imwrite("finish.png", output)
cap.release()
cv.destroyAllWindows()
