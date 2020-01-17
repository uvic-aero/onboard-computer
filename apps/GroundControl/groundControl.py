
import serial

class GroundControl():
    #Used to control the ground vehicle

    def __init__(self):


        groundControl = GroundControl()


        # open serial port
    	#ser = serial.Serial('/dev/ttyUSB0')



    def convert_to_binary(commands):
    # Do something to convert the commands to binary
    # Commands will be in a dictionary that looks like this

    binary_string = "<"


    if commands.get("180") == false:
    binary_string.append('0 ')
    else:
    binary_string.append('1 ')

    if commands.get("break") == false:
    binary_string.append('0 ')
    else:
    binary_string.append('1 ')

    #0 or 1 into string
    binary_string.append(commands.get("dir1") + " ")

    binary_string.append(commands.get("vel1") + " ")

    binary_string.append(commands.get("dir2") + " ")

    binary_string.append(commands.get("vel2") + " ")

    binary_string.append(">")

    return binary_string
​

    # not sure why 2 functions
    def send_command_to_arduino(command):


    return None

    ser.close()
