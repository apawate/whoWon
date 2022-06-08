from threading import Thread
import time
import cv2

# Setting up camera and resolution
slice_height = int(input("Enter image height: "))
slice_width = int(input("Enter image width: "))

cap = cv2.VideoCapture(0)
cap.set(3, slice_width)
cap.set(4, slice_height)
cap.set(cv2.CAP_PROP_FPS, 60)

frame_stream = []  # stores tuple of (unprocessed frame, timestamp)

# Setting height and width constants, and initializing the composite image
ret, temp_image = cap.read()
while not ret:
    ret, temp_image = cap.read()

composite_image = temp_image[0:slice_height, 0:1]
cv2.imshow('Waiting to start', composite_image)

while True:  # Pressing 's' starts the timer
    if cv2.waitKey(1) == ord('s'):
        start_time = time.time()
        cv2.destroyAllWindows()
        break


def stretch_image(image, x_factor, img_h, img_w):
    image = cv2.resize(image, (x_factor * img_w, img_h))
    return image


def process_time(number_time):
    if number_time < 60.0:
        seconds = str(round(number_time, 1))
        return seconds
    else:
        num_minutes = int(number_time / 60)
        seconds = round((number_time - (num_minutes * 60)), 1)
        if seconds < 10:
            combined_time = str(num_minutes) + ":0" + str(seconds)
        else:
            combined_time = str(num_minutes) + ":" + str(seconds)
        return combined_time


def capture_image():
    num_frame = 0
    while True:

        captured, frame = cap.read()  # Capturing image
        if captured:  # If a frame has been captured

            temp_time = time.time() - start_time  # Capturing timestamp
            frame_stream.append((frame, temp_time))  # Adding data to frame stream
            num_frame += 1

        if not cap.isOpened():
            FPS = num_frame / (frame_stream[-1][1])
            print("FPS: " + str(FPS))
            cap.release()

            break


def process_stream():
    prev_time = 0.0
    global composite_image
    while True:
        while len(frame_stream) > 0:

            # IMAGE PROCESSING
            full_frame = frame_stream[0][0]  # Taking frame value of first capture
            temp = full_frame[0:slice_height, 0:1]  # Slicing
            temp = stretch_image(temp, 5, slice_height, 1)  # Stretching
            composite_image = cv2.hconcat([temp, composite_image])  # Creating image
            cv2.imshow('WebCam', full_frame)  # Showing currently processing frame
            cv2.imshow('Composite', composite_image[0:slice_height, 0:1500])  # Showing selection of composite image

            # TIME LABELS
            frame_time = frame_stream[0][1]  # Taking timestamp of first capture
            if frame_time >= (prev_time + 0.5):  # If the timestamp warrants a label on the image
                str_time = "|" + process_time(frame_time)  # Format the time
                composite_image = cv2.putText(composite_image, str_time, (0, (slice_height - 3)), 1, 1, (0, 0, 255),
                                              1)  # Add text
                prev_time += 0.5  # Increment the requisite time

            print(frame_stream[0][1])
            frame_stream.pop(0)  # Removing processed frame
            print("finished frame adding")

        if cv2.waitKey(1) == ord('q'):  # Quitting when 'q' pressed
            cap.release()
            break


capture_thread = Thread(target=capture_image)
process_thread = Thread(target=process_stream)

capture_thread.start()
process_thread.start()

capture_thread.join()
process_thread.join()

cap.release()
cv2.destroyAllWindows()

cv2.imshow('finish cam', composite_image)

while True:
    if cv2.waitKey(1) == ord('f'):
        cap.release()
        cv2.destroyAllWindows()
        break
