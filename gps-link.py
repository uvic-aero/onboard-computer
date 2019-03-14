
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import argparse

# Function to arm
def arm():

  print "Basic pre-arm checks"
  # Don't try to arm until the vehicle is ready
  while not vehicle.is_armable:
    print " Waiting for vehicle to initialize..."
    time.sleep(1)
        
  print "Arming..."
  vehicle.armed = True

  while not vehicle.armed:
    print "Arming..."
    time.sleep(1)

parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='/dev/ttyAMA0')
args = parser.parse_args()

# Connect to the vehicle, creat vehicle object
print 'Connecting to vehicle on: %s' % args.connect
vehicle = connect(args.connect, baud = 921600, wait_ready = True)

# Arm the vehicle
arm()

print("Armed")

# Report GPS coordinates
while True:
    print "GPS: %s" % vehicle.gps_0
    time.sleep(1)

# Close vehicle object
vehicle.close()