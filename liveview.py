import socket
import asyncio
import urllib
import binascii
import io
import traceback
from PIL import Image

class Liveview:
    def __init__(self, camera_stream_url):
        self.started = False
        self.stopped = True
        self.out_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.connections = []
        self.server = None

        url_info = urllib.parse.urlparse(camera_stream_url)
        self.stream_hostname = url_info.hostname
        self.stream_port = url_info.port
        self.stream_path = url_info.path

    async def start(self):
        if self.started is False and self.stopped is True:
            self.stopped = False
            await self._start_server()
            await self._start_client()
            self.started = True

    async def _start_server(self):
        print("Starting liveview server")
        if self.server is None:
            self.server = await asyncio.get_event_loop().create_task(asyncio.start_server(self.client_connected, host="127.0.0.1", port=5000, family=socket.AF_INET))
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
        skipped_bytes = 0

        while True:
            if self.stopped:
                # TODO : ffmpeg.stop()
                self.connections = []
                self.server.close()
                self.server = None
                break
            
            data = await reader.read(1)

            if len(data) == 0:
                continue

            start_byte = data[0]

            # 255 dictates start of new header+payload
            if start_byte != 255:
                skipped_bytes += 1
                continue

            # Read rest of info header
            data = await reader.read(7)

            # Sanity check the payload type
            payload_type = data[0] # 1 or 2

            if payload_type != 1:
                skipped_bytes += 1
                continue

            sequence_number = int(binascii.hexlify(data[1:3]), 16)
            time_stamp = int(binascii.hexlify(data[3:7]), 16)

            # Read payload header
            data = await reader.readexactly(128)

            start_code = int(binascii.hexlify(data[0:4]), 16)
            jpeg_data_size = int(binascii.hexlify(data[4:7]), 16)
            padding_size = data[7]

            _image_width = int(binascii.hexlify(data[7:9]), 16)
            _image_height = int(binascii.hexlify(data[9:11]), 16)

            # Read actual payload
            raw_image = await reader.readexactly(jpeg_data_size)

            if padding_size > 0:
                await reader.readexactly(padding_size)

            await self.broadcast_image(raw_image)

            print("Frame: %s" % frames)
            frames += 1

    async def client_connected(self, _reader, writer):
   
        print("Added new streaming client")

        message = "\r\n".join([
            'HTTP/1.1 200 OK',
            'Content-Type: multipart/x-mixed-replace;boundary=frame',
            '', ''])

        writer.write(message.encode())
        await writer.drain()

        self.connections.append(writer)

        # Disabled until a better method of closing the connection is written
        '''
        while writer.transport.is_closing() is False:
            await asyncio.sleep(1)
            continue

        writer.close()
        self.connections.remove(writer)
        '''

    async def broadcast_image(self, image):

        message = b'--frame\r\nContent-Type: image/jpeg\r\nContent-Length: %d' % len(image) + b'\r\n\r\n' + image + b'\r\n'

        for conn in self.connections:
            if conn.transport.is_closing() is True:
                continue

            try:
                conn.write(message)
                await conn.drain()
            except:
                traceback.print_exc()
                conn.close()

    async def stop(self):
        if self.started is True and self.stopped is False:
            self.stopped = True
            self.started = False
