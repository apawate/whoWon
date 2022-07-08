import cv2
import numpy as np

stream = cv2.VideoCapture("http://10.0.1.13:5000")
counter = 0


while True:
    state, img = stream.read()
    #cv2.imshow('Webcam', img)
    counter = counter + 1
    print(counter)
    if cv2.waitKey(1) == ord('q'):
        break

stream.release()
cv2.destroyAllWindows()
