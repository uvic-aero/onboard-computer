
import serial

class GroundControl():
    #Used to control the ground vehicle

    def __init__(self):

        self.id = 0


        # open serial port
        self.ser = serial.Serial('/dev/ttyUSB0')



    def convert_to_binary(self, commands):
        # Do something to convert the commands to binary
        # Commands will be in a dictionary that looks like this

        self.id += 1

        binary_string = "<"

        binary_string += str(self.id) + ' '

        if commands.get("180") == False:
            binary_string += '0 '
        else:
            binary_string += '1 '

        if commands.get("break") == False:
            binary_string += '0 '
        else:
            binary_string += '1 '

        #0 or 1 into string
        binary_string += str(commands.get("dir1")) + " "

        binary_string += str(commands.get("vel1")) + " "

        binary_string += str(commands.get("dir2")) + " "

        binary_string += str(commands.get("vel2")) + " "

        binary_string += r">"

        return binary_string

    # not sure why 2 functions
    def send_command_to_arduino(self, commands):

        self.ser.write(self.convert_to_binary(commands).encode('utf-8'))
        print(commands)
        print(self.convert_to_binary(commands))
        return None

    def serial_close(self):
        self.ser.close()


# Test functions
gc = GroundControl()
commands = {
    '180': False,
    'break': False,
    'dir1': 1,
    'vel1': 100,
    'dir2': 0,
    'vel2': 50
    }
gc.send_command_to_arduino(commands)
gc.serial_close()
