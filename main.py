from multiprocessing import Process, Manager, Value # Import necessary multiprocessing
import time
import cv2

# Setting up camera and resolution
slice_height = int(input("Enter image height: "))
slice_width = int(input("Enter image width: "))

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("http://10.0.1.13:5000") # Capture from IP of the camera (change if needed)
cap.set(3, slice_width)
cap.set(4, slice_height)
cap.set(cv2.CAP_PROP_FPS, 1000)  # Set frame rate to max possible

frame_stream = []  # stores tuple of (unprocessed frame, timestamp)

# Setting height and width constants, and initializing the composite image
ret, temp_image = cap.read()
while not ret:
    ret, temp_image = cap.read()

composite_image = temp_image[0:slice_height, 0:1]
cv2.imshow('Waiting to start', composite_image)

# Checking frame rate to determine stretching factor

frame_counter = 0  # is also the fps
fps_elapsed_time = 0
fps_start_time = time.time()
while fps_elapsed_time < 1.0:  # checking number of frames in one second
    frame_returned, frame = cap.read()
    if frame_returned:
        frame_counter += 1
    fps_elapsed_time = time.time() - fps_start_time

stretching_factor = int(240/frame_counter)  # stretching to match 240 fps

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


def capture_image(frame_stream, diff):
    num_frame = 0
    temp_time = 0
    while True:
        print("capture " + str(len(frame_stream)))

        captured, frame = cap.read()  # Capturing image
        if captured:  # If a frame has been captured
            diff.value = time.time() - start_time - temp_time # Find the delay between the frames (internet speed)
            if temp_time == 0:
                diff.value = 1 # Quick and dirty fix, will need to be updated later
            temp_time = time.time() - start_time  # Capturing timestamp
            print("Time " + str(temp_time))
            frame_stream.append((frame, temp_time))  # Adding data to frame stream
            print("Frame delay " + str(diff.value))
            num_frame += 1

        if not cap.isOpened():
            FPS = num_frame / (frame_stream[-1][1])
            print("FPS: " + str(FPS))
            cap.release()

            break


def process_stream(frame_stream, diff):
    prev_time = 0.0
    time.sleep(1) # Time buffer to let the stream start
    global composite_image
    while True:
        while 1:
            time.sleep(diff.value) # Delay by the average delay between frames, prevents zero-frame trap
            print("process", len(frame_stream)) 
            # IMAGE PROCESSING
            full_frame = frame_stream[0][0]  # Taking frame value of first capture
            temp = full_frame[0:slice_height, 0:1]  # Slicing
            temp = stretch_image(temp, stretching_factor, slice_height, 1)  # Stretching
            composite_image = cv2.hconcat([temp, composite_image])  # Creating image
            cv2.imwrite("a.png", full_frame)
            cv2.imwrite("b.png", composite_image[0:slice_height, 0:1500]) # Debugging images
            #cv2.imshow('WebCam', full_frame)  # Showing currently processing frame
            #cv2.imshow('Composite', composite_image[0:slice_height, 0:1500])  # Showing selection of composite image

            # TIME LABELS
            frame_time = frame_stream[0][1]  # Taking timestamp of first capture
            if frame_time >= (prev_time + 0.5):  # If the timestamp warrants a label on the image
                str_time = "|" + process_time(frame_time)  # Format the time
                composite_image = cv2.putText(composite_image, str_time, (0, (slice_height - 3)), 1, 1, (0, 0, 255),
                                              1)  # Add text
                prev_time += 0.5  # Increment the requisite time
            cv2.imwrite("finish3.png", composite_image)
            frame_stream.pop(0)  # Removing processed frame
            print("finished frame adding")

        if cv2.waitKey(1) == ord('q'):  # Quitting when 'q' pressed
            cap.release()
            break


with Manager() as manager: 
    num = Value('d', 0.0) # Setting up frame delay variable as a multiprocessing variable
    stream = manager.list() # Setting up frame stream variable as a multiprocessing variable
    capture_thread = Process(target=capture_image, args=(stream,num))
    process_thread = Process(target=process_stream, args=(stream,num)) # Initializing with shared variables
    
    capture_thread.start()
    process_thread.start()
    
    capture_thread.join()
    process_thread.join()
    
cap.release()
cv2.destroyAllWindows()
    
cv2.imwrite('finish4.png', composite_image) # Writing finish camera to disk

while True:
    if cv2.waitKey(1) == ord('f'):
        cap.release()
        cv2.destroyAllWindows()
        break
