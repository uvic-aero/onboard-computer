import unittest
from apps.GroundControl.groundControl import ground_control

# Tests are run in alphabetical order, the message id will increment accordingly
class TestSerial(unittest.TestCase):

    def test_send_message(self):
        commands= {
                    "180": False,
                    "brake": False,
                    "dir1": 1,
                    "dir2": 1,
                    "vel1": 150,
                    "vel2": 150 
                }

        response = ground_control.send_command_to_arduino(commands)

        self.assertEqual(response, "<1 0 0 1 150 1 150>")

    def test_two_messages(self):
        commands= {
                    "180": False,
                    "brake": False,
                    "dir1": 1,
                    "dir2": 0,
                    "vel1": 25,
                    "vel2": 130 
                }
        
        response = ground_control.send_command_to_arduino(commands)

        self.assertEqual(response, "<2 0 0 1 25 0 130>")

if __name__ == '__main__':
    unittest.main()
