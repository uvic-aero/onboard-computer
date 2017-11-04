import asyncio
import requests
import functools
import traceback
import time
import unittest
import warnings
from camera import Camera


def ignore_warnings(test_func):
    """Ignore the resource wanring request due to unharmful persistent socket designed in requests library"""
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)
    return do_test

async def sleep():
    await asyncio.sleep(5)

async def task_wrapper(loop, task_queue):
    for task in task_queue:
        await asyncio.ensure_future(task())
    loop.stop()

class camera_test(unittest.TestCase):
    @ ignore_warnings
    def test_connection_1(self):
        # Build phase
        camera = Camera()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        task_queue = [camera.check_and_start_connection]
        
        # Operate phase
        asyncio.ensure_future(task_wrapper(loop, task_queue)) ###
        loop.run_forever()
        loop.close()

    @ ignore_warnings
    def test_start_record_mode_2(self):
        # Build phase
        camera = Camera()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        task_queue = [camera.check_and_start_connection, camera.set_record_mode]
        
        # Operate phase
        asyncio.ensure_future(task_wrapper(loop, task_queue)) ###
        loop.run_forever()
        loop.close()

    @ ignore_warnings
    def test_take_one_picture_3(self):
        # Build phase
        camera = Camera()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        task_queue = [camera.check_and_start_connection, camera.set_record_mode, camera.take_picture]

        # Operate phase
        asyncio.ensure_future(task_wrapper(loop, task_queue)) ###
        loop.run_forever()
        loop.close()

    @ ignore_warnings
    def test_take_ten_pictures_4(self):
        # Build phase
        camera = Camera()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        take_ten_pictures_task = [camera.take_picture for _ in range(10)]
        task_queue = [camera.check_and_start_connection, camera.set_record_mode]
        task_queue.extend(take_ten_pictures_task)

        # Operate phase
        asyncio.ensure_future(task_wrapper(loop, task_queue)) ###
        loop.run_forever()
        loop.close() 

    @ ignore_warnings
    def test_take_one_picture_and_zoom_in_and_take_another_one_and_zoom_out_5(self):
        # Build phase
        camera = Camera()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        task_queue = [
        camera.check_and_start_connection,
        camera.set_record_mode,
        camera.take_picture,
        camera.zoom_in,
        camera.zoom_in,
        camera.zoom_in,
        camera.take_picture,
        camera.zoom_out,
        camera.check_camera_status,
        camera.zoom_out,
        camera.check_camera_status,
        camera.zoom_out
        ]
        # Operate phase
        asyncio.ensure_future(task_wrapper(loop, task_queue)) ###
        loop.run_forever()
        loop.close()

    @ ignore_warnings
    def test_start_liveview_and_sleep_and_zoom_in_and_zoom_out_and_stop_liveview_and_zoom_in_and_take_picture_6(self):
        # Build phase
        camera = Camera()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        task_queue = [
        camera.check_and_start_connection, 
        camera.set_record_mode,
        camera.start_liveview,
        sleep,
        camera.zoom_in,
        camera.zoom_in,
        camera.zoom_out,
        camera.stop_liveview,
        camera.zoom_in,
        camera.take_picture
        ]
        # Operate phase
        asyncio.ensure_future(task_wrapper(loop, task_queue)) ###
        loop.run_forever()
        loop.close()

    @ ignore_warnings
    def test_start_liveview_and_sleep_and_stop_liveview_and_start_liveview_and_sleep_and_stop_liveview_7(self):
        # Build phase
        camera = Camera()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        task_queue = [
        camera.check_and_start_connection, 
        camera.set_record_mode,
        camera.start_liveview,
        sleep,
        camera.stop_liveview,
        camera.start_liveview,
        sleep,
        camera.stop_liveview
        ]
        # Operate phase
        asyncio.ensure_future(task_wrapper(loop, task_queue)) ###
        loop.run_forever()
        loop.close()

'''
 class obc_test(unittest.TestCase): TODO

'''


if __name__ == "__main__":
	unittest.main()
