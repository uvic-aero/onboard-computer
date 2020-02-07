
import serial

MESSAGE_START = "<"
MESSAGE_END = ">"
ENDCODING = "utf-8"
SERIAL_PORT = "/dev/ttyUSB0"

#Used to control the ground vehicle
class GroundControl():
    def __init__(self):
        self.id = 0

        # open serial port
        self.ser = serial.Serial(SERIAL_PORT)


    # Convert commands to string with format
    # <id(int) 180(0,1) break(0,1) dir1(0,1), vel1(0-255), dir2(0,1), vel2(0-255) >
    def convert_to_string(self, commands):
        command_string = MESSAGE_START

        command_string += str(self.id) + " "

        if commands.get("180") == False:
            command_string += "0 "
        else:
            command_string += "1 "

        if commands.get("break") == False:
            command_string += "0 "
        else:
            command_string += "1 "

        #0 or 1 into string
        command_string += str(commands.get("dir1")) + " "

        command_string += str(commands.get("vel1")) + " "

        command_string += str(commands.get("dir2")) + " "

        command_string += str(commands.get("vel2")) + " "

        command_string += MESSAGE_END

        return command_string
    

    # Waits for message start and returns the message
    def get_response(self):
        response_buffer = ""
        finished = False

        while(not finished):
            if(self.ser.read().decode(ENDCODING) == MESSAGE_START):
                response_buffer += self.ser.read_until(MESSAGE_END.encode(ENDCODING)).decode(ENDCODING)
                finished = True
        
        return response_buffer


    # Send commands to arduino and print response
    # Commands should be a dictionary that looks like
    # {180: [True, False], break: [True, Flase], dir1: [0,1], vel1: [0-255], dir2: [0,1], vel2: [0-255]}
    def send_command_to_arduino(self, commands):
        self.id += 1
        to_send = self.convert_to_string(commands).encode(ENDCODING)
        self.ser.write(to_send)
        print(self.get_response())


    # Close serial connection
    def close_serial(self):
        self.ser.close()

# Create singleton instance
gc = GroundControl()
