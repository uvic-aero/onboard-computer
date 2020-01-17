import cv2
import base64
import sys
import time
import importlib

class Capture:

    def __init__(self):
        pass
    def show_webcam(mirror=False):
        cam = cv2.VideoCapture(0)
        while True:
            ret_val, frame = cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, (0, 0), fx=0.1, fy=0.1)
            # img = cv2.imencode('.jpg', gray)[1]
            # buffer = base64.b64encode(img)
            img=gray
            if mirror: 
                img = cv2.flip(img, 1)
            cv2.imshow('my webcam', img)
            if cv2.waitKey(1) == 27: 
                break  # esc to quit
        cv2.destroyAllWindows()
        # if buffer is None:
        #     print("buffer is None")
            # continue
            # We send back the buffer to the client

    def use_pycam():
        #check if pi
        if importlib.find_loader("picamera"):
            found_picamera = True
             # import the necessary packages
            from picamera import PiCamera
            from picamera.array import PiRGBArray
        # initialize the camera and grab a reference to the raw camera capture
        camera = PiCamera()
        camera.resolution = (3280, 2464)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(640, 480))
        
        # allow the camera to warmup
        time.sleep(0.1)
        
        # capture frames from the camera
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            image = frame.array
        
            # show the frame
            cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF
        
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)
        
            # if the `q` key was pressed, break from the loop
            # if key == ord("q"):
            #     break
            if cv2.waitKey(1) == 27:
                break
            cv2.destroyAllWindows()

    def capture_video(use_picam=False):
        if not use_picam:
            show_webcam()

    if __name__ == "__main__":
        print("kicking off webcam video capture")
        #use_pycam()
        show_webcam()