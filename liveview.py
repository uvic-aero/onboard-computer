import socket
import asyncio
import urllib
import binascii
import io
from PIL import Image

class Liveview:
    def __init__(self, camera_stream_url):
        self.started = False
        self.out_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.connections = []

        url_info = urllib.parse.urlparse(camera_stream_url)

        self.stream_hostname = url_info.hostname
        self.stream_port = url_info.port
        self.stream_path = url_info.path

    async def start(self):
        if self.started is False:
            self._start_server()
            await self._start_client()
            self.started = True

    def _start_server(self):
        print("Starting liveview server")
        asyncio.get_event_loop().create_task(asyncio.start_server(self.client_connected, host="127.0.0.1", port=5000, family=socket.AF_INET))
        #server = self.loop.run_until_complete(coro)
        print("Started liveview server on 127.0.0.1:5000")

    async def _start_client(self):

        # Open TCP connection to liveview host
        reader, writer = await asyncio.get_event_loop().create_task(asyncio.open_connection(host=self.stream_hostname, port=self.stream_port))

        # Handle liveview I/O
        asyncio.get_event_loop().create_task(self.stream_connection(reader, writer))

    async def stream_connection(self, reader, writer):
        print("Connected to camera liveview stream")

        # Send raw HTTP request to initiate data flow
        request = "\r\n".join([
            'GET %s HTTP/1.1' % self.stream_path,
            'HOST: %s:%s' % (self.stream_hostname, self.stream_port),
            'ACCEPT: */*',
            '', ''])

        writer.write(request.encode())

        # Read initial HTTP response
        # TODO: Parse HTTP OK or potential error
        # b'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nTransfer-Encoding: chunked\r\n\r\n6788\r\n'
        data = await reader.read(95)

        frames = 1

        while True:
            data = await reader.readexactly(8)

            start_byte = data[0]

            if start_byte != 255:
                continue

            #payload_type = data[1] # 1 or 2
            #sequence_number = int(binascii.hexlify(data[2:4]), 16)
            #time_stamp = int(binascii.hexlify(data[4:8]), 16)

            #print(start_byte, payload_type, sequence_number, time_stamp)

            data = await reader.readexactly(128)

            #start_code = int(binascii.hexlify(data[0:4]), 16)
            jpeg_data_size = int(binascii.hexlify(data[4:7]), 16)
            padding_size = data[7]

            #reserved_1 = int(binascii.hexlify(data[8:12]), 16)
            #flag = data[12] # 0x00
            #reserved_2 = int(binascii.hexlify(data[13:]), 16)

            #print(start_code, jpeg_data_size, padding_size)

            raw_image = await reader.readexactly(jpeg_data_size)

            #Image.open(io.BytesIO(raw_image)).save('image.jpg')

            if padding_size > 0:
                await reader.readexactly(padding_size)

            await self.broadcast_image(raw_image)

            print("Frame: %s" % frames)
            frames += 1

    async def client_connected(self, _reader, writer):

        print("Added new streaming client")

        message = "\r\n".join([
            'HTTP/1.1 200 OK',
            'Content-Type: multipart/x-mixed-replace; boundary=frame',
            '', ''])

        writer.write(message.encode())
        await writer.drain()

        self.connections.append(writer)

        while writer.transport.is_closing() is False:
            await asyncio.sleep(1)
            continue

        writer.close()
        self.connections.remove(writer)

    async def broadcast_image(self, image):

        print("Sending img")

        message = b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n'

        #print(message)

        for conn in self.connections:
            conn.write(message)
            await conn.drain()

            print("Sent img")
