#!/usr/bin/env python3

from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

def gen_frames():
    global camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()
        if not success:
            print("fail")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


camera = cv2.VideoCapture(0)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=False)
