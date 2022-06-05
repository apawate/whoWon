from flask import Flask, render_template, request, Response
import cv2 

app = Flask('app')

camera = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace;boundary=frame')



app.run('0.0.0.0', port=3000)
