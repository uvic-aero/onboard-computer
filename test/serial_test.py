import unittest
from apps.GroundControl.groundControl import ground_control


class TestSerial(unittest.TestCase):

    def test_send_message(self):
        commands= {
                    "180": False,
                    "break": False,
                    "dir1": 1,
                    "dir2": 1,
                    "vel1": 150,
                    "vel2": 150 
                }

        response = ground_control.send_command_to_arduino(commands)

        self.assertEquals(response, "")


if __name__ == '__main__':
    unittest.main()
