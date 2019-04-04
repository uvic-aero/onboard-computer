from dronekit import *
from pymavlink import mavutil
import argparse
import serial

class TelemData:
  
  def __init__(self):
    self.connect(args)
    self.status = 'down' #this status is used to check if a service is functioning normaly or not
  
  def start(self):
    print('starting telemData')
    self.status = 'running'
    # this function will at least connect to pixhawk for future telem data retrieval.
    parser = argparse.ArgumentParser()
    parser.add_argument('--connect', default='/dev/ttyAMA0')
    parser.add_argument('--baud', default='115200')
    args = parser.parse_args()
    self.connect(args)

  def stop(self):
    print('stopping videoDisplay')
    self.status = 'down'
    # this function should kill the connection to the pixhawk and 
    # any other processes it has started.
    self.disconnect()

  def check_status(self):
    # check all possible processes that may not be working properly, make sure they return
    # expected values.
    # return list of broken services.
    if(self.connection_status)
      print('Status: Active')
      print('GPS connection state: %s' % vehicle.gps_0)
    else
      print('Status: Broken (see above for details)')

  # Connect to the vehicle
  def connect(self, args):
    print('Connecting to aircraft via: %s' % args.connect)

    try:
    self.vehicle = connect(args.connect, baud = args.baud, wait_ready = True)
    self.connection_status = 1
    # Dronekit Error
    except dronekit.APIException:
        print 'The connection has timed out.'
        self.connection_status = 0
        self.status = 'pixhawk connection broken'

    # Other error
    except:
        print 'An unexpected error occured'
        self.connection_status = 0
        self.status = 'pixhawk connection broken'

  # Close vehicle connection
  def disconnect(self):
    self.vehicle.close()
    self.connection_status = 0

  def getLat(self):
    return self.vehicle.location.global_relative_frame.lat

  def getLon(self):
    return self.vehicle.location.global_relative_frame.lon

  def getAlt(self):
    return self.vehicle.location.global_relative_frame.alt

  def getGPSLocation(self):
    return {"lat":self.getLat, "lon":self.getLon, "alt":self.getAlt}

telemData = TelemData()

# Report GPS coordinates (use for testing)
#while True:
#    print("GPS: %s" % vehicle.location.global_relative_frame)
#    print("GPS: %s" % vehicle.gps_0)
#    time.sleep(1)