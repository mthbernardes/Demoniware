import cv2
import socket
import numpy
import sys

host = ''
port = sys.argv[1]

while True:
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,port))
    s.listen(1)
    conn, addr = s.accept()
    message = []
    while True:
        d = conn.recv(1024 *1024)
        if not d: break
        else: message.append(d)
    data = ''.join(message)
    stringData = numpy.fromstring(data, numpy.uint8)

    decimg = cv2.imdecode(stringData, 1)
    cv2.imshow("Remote Webcam", decimg)


    if cv2.waitKey(5) == 27: break

cv2.destroyAllWindow()
