import time
import cv2
import numpy as np
from threading import Thread

def stretch_image(image, x_factor, img_h, img_w):
    image = cv2.resize(image, (x_factor * img_w, img_h))
    return image


def process_time(number_time):
    if (number_time < 60.0):
        seconds = str(round(number_time, 0))
        return seconds
    else:
        num_minutes = int(number_time / 60)
        seconds = round((number_time - (num_minutes * 60)), 0)
        if (seconds < 10):
            combined_time = str(num_minutes) + ":0" + str(seconds)
        else:
            combined_time = str(num_minutes) + ":" + str(seconds)
        return combined_time


# Setting up camera and resolution
cap = cv2.VideoCapture("http://10.0.1.13:5000")
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(3, 480)
cap.set(4, 360)

# Setting height and width constants, and initializing the composite image
ret, temp_image = cap.read()
slice_height = temp_image.shape[0]
slice_width = temp_image.shape[1]
composite_image = temp_image[0:slice_height, 0:1]
cv2.imshow('Waiting to start', composite_image)

# Pressing 's' starts the timer
while True:
    if cv2.waitKey(1) == ord('s'):
        start_time = time.time()
        cv2.destroyAllWindows()
        break

prev_time = 0.0  # helps increment timestamps at consistent intervals

# Reading
while True:

    # Assembling
    ret, frame = cap.read()
    temp = frame[0:slice_height, 0:1]
    temp = stretch_image(temp, 10, slice_height, 1)
    composite_image = cv2.hconcat([temp, composite_image])
    #cv2.imshow('WebCam', frame)
    #cv2.imshow('Composite', composite_image)

    # TIMER
    elapsed_time = time.time() - start_time
    if (elapsed_time > (prev_time + 0.5)):
        str_time = "|" + process_time(elapsed_time)
        # add text
        composite_image = cv2.putText(composite_image, str_time, (0, (slice_height - 3)), 1, 0.5, (0, 0, 255), 1)
        prev_time += 0.5
    print(elapsed_time)
    cv2.imwrite('finish3.png', composite_image)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

cv2.imwrite('finish3.png', composite_image)


while True:
    if cv2.waitKey(1) == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
