from flask import Flask,render_template, Response
import cv2
 
app=Flask(__name__)
camera=cv2.VideoCapture(0)
 
def generate_frames(): 
    while True:
        #reading the camera frame
        success,frame=camera.read()  #it gives 2 parameter so storing it in 2, success and frame, success is a booleon var and frame comtains the camera frames
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg',frame) #encodes image into memory buffer
            frame=buffer.tobytes()
 
        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
               #when the images are in bytes you need to change the content type
               #taken from open cv documentation
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
    app.run(debug=True)