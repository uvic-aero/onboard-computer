import unittest
import socket
from apps.VideoStream.videoStream import videoStream
import time

class TestVideoStream(unittest.TestCase):

    # def test_server_start(self):
    #     stream = VideoStream()
    #     stream.start()
    #     self.assertEqual(stream.status, "running")
    #     stream.stop()
    #     time.sleep(2)

    # def test_make_connection(self):
    #     stream = VideoStream()
    #     stream.start()
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     address = ('0.0.0.0', stream.port)
    #     sent = sock.sendto("get".encode('utf-8'), address)
    #     self.assertEqual(len(stream.connections.connections), 1)
    #     stream.stop()

    def test_a(self):
        vs = videoStream
        vs.start()
        time.sleep(3)
        vs.stop()
        time.sleep(3)
        self.assertEqual(1, 1)
    
    def test_b(self):
        vs = videoStream
        vs.start()
        time.sleep(3)
        vs.stop()
        time.sleep(3)
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
