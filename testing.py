import cv2
import numpy as np

stream = cv2.VideoCapture("http://10.0.1.12:3000")

while True:
    state, img = stream.read()
    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

stream.release()
cv2.destroyAllWindows()
