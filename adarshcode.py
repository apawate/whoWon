import cv2
import numpy as np

camera = cv2.VideoCapture(0)

def stretch_image(image, x_factor, img_h, img_w):
    image = cv2.resize(image, (5*img_w, img_h))
    return image


ret, temp_image = camera.read()
image_height = temp_image.shape[0]
composite_image = temp_image[0:image_height, 0:1]

while True:

    ret, frame = camera.read()
    temp = frame[0:image_height, 0:1]
    composite_image = cv2.hconcat([composite_image, temp])
    cv2.imshow('WebCam', frame)
    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

image_width = composite_image.shape[1]
composite_image = stretch_image(composite_image, 5, image_height, image_width)
cv2.imshow('finish cam', composite_image)

while True:
    if cv2.waitKey(1) == ord('q'):
        camera.release()
        cv2.destroyAllWindows()
        break
