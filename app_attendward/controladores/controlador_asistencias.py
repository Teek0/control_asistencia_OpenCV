from flask import render_template, Response
from app_attendward import app
import cv2

def generate():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    while True:
        ret, frame = cap.read()
        if ret:
            gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

@app.route('/captura_asistencia', methods=['GET'])
def get_all_alumnos():
    return render_template('captura_asistencia.html')
@app.route('/video_feed', methods=['GET'])
def video_feed():
    print ("video_feed")
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
