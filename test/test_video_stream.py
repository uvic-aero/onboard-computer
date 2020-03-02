import unittest
import socket
from apps.VideoStream.videoStream import videoStream
import time

class TestVideoStream(unittest.TestCase):

    def test_server_start(self):
        videoStream.start()
        self.assertEqual(videoStream.status, "running")
        videoStream.stop()
        time.sleep(2)

    def test_server_stop(self):
        videoStream.start()
        videoStream.stop()
        self.assertEqual(videoStream.status, "down")
        time.sleep(2)
    ''' 
    def test_make_connection(self):
        videoStream.start()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = ('0.0.0.0', videoStream.port)
        sent = sock.sendto("get".encode('utf-8'), address)
        videoStream.stop()
        time.sleep(2)
        self.assertEqual(len(videoStream.connections.connections), 1)
    '''
if __name__ == '__main__':
    unittest.main()
