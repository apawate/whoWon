import cv2
stream = cv2.VideoCapture("http://10.0.1.12:3000")

while True:
    img = stream.read()
    print(img)
