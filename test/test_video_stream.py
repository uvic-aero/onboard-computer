import unittest
import socket
from apps.VideoStream.videoStream import videoStream
import time

class TestVideoStream(unittest.TestCase):

    def test_server_start(self):
        self.assertEqual(videoStream.status, "down")
        videoStream.start()
        self.assertEqual(videoStream.status, "running")
        videoStream.stop()

    def test_make_connection(self):
        videoStream.start()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = ('0.0.0.0', videoStream.port)
        while len(videoStream.connections.connections) < 1:
            sock.sendto("get".encode('utf-8'), address)
        self.assertEqual(len(videoStream.connections.connections), 1)
        videoStream.stop()
        sock.close()

if __name__ == '__main__':
    unittest.main()
