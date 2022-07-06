from flask import Flask, render_template, Response
from camera import Camera

app = Flask(__name__)

def gen(camera):
    while True:
        frame = camera.get_frame() # Get frame from camera
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') # Return without exiting

@app.route('/')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame') # Create updating HTML video stream based on gen function

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
