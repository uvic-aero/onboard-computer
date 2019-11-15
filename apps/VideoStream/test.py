from VideoStream import videoStream

cap = cv2.VideoCapture(0)


while True:

    ret, frame = cap.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),1]
    encimg = cv2.imencode('.jpg', grey, encode_param)[1].tostring()
    videoStream.send_frame(encimg)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
videoStream.socket.close()
