import cv2
import numpy as np

camera = cv2.VideoCapture("udp://10.0.1.12:3000")

while True:
    ret, frame = camera.read()
    cv2.imshow('Webcam', frame)

