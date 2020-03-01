import unittest
import socket
from apps.VideoStream.videoStream import videoStream

class TestVideoStream(unittest.TestCase):

    def __init__(self):
        self.stream = VideoStream()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = ('0.0.0.0', self.stream.port) 

    def test_server_start(self):
        self.assertEqual(self.stream.status, "running")

    def test_make_connection(self):
        sent = self.sock.sendto("get".encode('utf-8'), self.address)
        self.assertEqual(len(self.stream.connections.connections), 1)
