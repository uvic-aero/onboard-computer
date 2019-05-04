import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import re
import math
import time
import base64
import requests

groundstation_url = "http://192.168.0.100:24002"
groundstation_url = "http://localhost:24002"

def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value
    return exif_data

def _get_if_exist(data, key):
    if key in data:
        return data[key]
        
    return None

def convert_to_degrees(val):
    digits = int(math.log10(val[1]))+1
    decimal = val[1] / 10 ** digits
    return val[0] + decimal

def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:        
        gps_info = exif_data["GPSInfo"]
        print(gps_info)
        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')
        convert_to_degrees(gps_latitude)
        '''
        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            #lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat = 0 - lat

            #lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon
        '''
    return convert_to_degrees(gps_latitude), -1 * convert_to_degrees(gps_longitude)

# takes filename, sends image to groundstation
def send_image(filename):
    # check that file is actually an image
    timestamp = time.time() * 1000

    if not re.match("^.*jpg$", filename):
        print('not an image')
        return
    path = './images/' + filename
    img = Image.open(path)
    telem = get_lat_lon(get_exif_data(img))
    telemetry = {
        'lat': telem[0],
        'lon': telem[1],
        'alt': 0,
    }
    print(get_lat_lon(get_exif_data(img)))

    image = open(path, 'rb')
    img = base64.b64encode(image.read())
    payload = {
        'timestamp': timestamp,
        'image': img.decode('utf-8', "ignore"),
        'telemetry': telemetry
    }
    requests.post(groundstation_url + '/images', json=payload)
    print('successfully sent image to the groundstation.')
    return True

# get all the files in the images/ dir
for root, dirs, files in os.walk('./images'): 
    for filename in files: 
        send_image(filename)

'''    
def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)
'''
