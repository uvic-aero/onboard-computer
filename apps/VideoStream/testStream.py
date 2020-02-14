from videoStream import videoStream
import cv2

cap = cv2.VideoCapture(0)
vs = videoStream
vs.start()

while True:

    ret, frame = cap.read()
    vs.broadcast(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
videoStream.socket.close()
