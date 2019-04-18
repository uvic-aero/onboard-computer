from dronekit import * 
from pymavlink import mavutil
import argparse
import serial

class TelemData:
    
    def __init__(self):
        self.status = 'down' #this status is used to check if a service is functioning normaly or not
        self.vehicle = None
    
    def start(self):
        print('starting telemData')
        self.status = 'running'
        # this function will at least connect to pixhawk for future telem data retrieval.
        parser = argparse.ArgumentParser()
        parser.add_argument('--connect', default='/dev/serial0')
        parser.add_argument('--baud', default='115200')
        args = parser.parse_args()
        self.connect(args)

    def stop(self):
        print('stopping Telemetry Data')
        self.status = 'down'
        # this function should kill the connection to the pixhawk and 
        # any other processes it has started.
        self.disconnect()

    def check_status(self):
        # check all possible processes that may not be working properly, make sure they return
        # expected values.
        # return list of broken services.
        if(self.connection_status):
            print('Status: Active')
            print('GPS connection state: %s' % vehicle.gps_0)
        else:
            print('Status: Broken (see above for details)')

    # Connect to the vehicle
    def connect(self, args):
        print('Connecting to aircraft via: %s' % args.connect)

        try:
            self.vehicle = connect(args.connect, baud = 921600, wait_ready = True)
            self.connection_status = 1
            # Dronekit Error
        except dronekit.APIException:
                print ('The connection has timed out.')
                self.connection_status = 0
                self.status = 'pixhawk connection broken'

        # Other error
        except:
                print ('An unexpected error occured')
                self.connection_status = 0
                self.status = 'pixhawk connection broken'

    # Close vehicle connection
    def disconnect(self):
        self.vehicle.close()
        self.connection_status = 0

    # Use for testing gps signal and telemetry data retrieval. WARNING: this method creates an infinite loop.
    def gps_test(self):
        pass
        while True:
            time.sleep(1)

    def getLat(self): # Get vehicle latitude
        if not self.vehicle:
            return 48.4284
        return str(self.vehicle.location.global_relative_frame.lat)

    def getLon(self): # Get vehicle longitude
        if not self.vehicle:
            return -123.3656
        return str(self.vehicle.location.global_relative_frame.lon)

    def getAlt(self): # Get vehicle altitude
        if not self.vehicle:
            return 0
        return self.vehicle.location.global_relative_frame.alt

    def get_location(self): # Get vehicle postion (Returns dict of lat,long, and alt)
        return {"lat":self.getLat(), "lon":self.getLon(), "alt":self.getAlt()}

telemData = TelemData()
