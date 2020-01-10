import serial

class GroundControl():
        #Used to control the ground vehicle

        def __init__(self):
            # TODO: Create and Calibrate Motor Controllers
                pass
        def start(self):
            ser = serial.Serial("/dev/ttyv5")
            print("Serial Name: ", ser.name)
            ser.close()

groundControl = GroundControl()
