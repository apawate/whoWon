import cv2
import urllib.request
import numpy as np
req = urllib.request.urlopen('10.0.1.12:3000')
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1)
cv2.imshow('Webcam', img)
if cv2.waitKey() & 0xff == 27: quit()
