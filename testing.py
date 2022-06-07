import cv2
import numpy as np
from urllib.request import urlopen


def url_to_image(url):

    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image


while True:
    frame = url_to_image("http://10.0.1.15:3000")
    cv2.imshow('Webcam', frame)

