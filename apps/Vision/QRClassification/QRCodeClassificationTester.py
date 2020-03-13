from QRCodeClassification import QRCodeClassification
import cv2
import os

"""
simple test file for QRCodeClassification. takes an image as input, converts it to nparray subimages and then returns images as jpgs
"""

tmp = QRCodeClassification()

subimages = tmp.split_frames("0.jpg")

directory = os.fsencode("./nparray-to-image").decode()
count = 0
for subimage in subimages:
    cv2.imwrite(f"./{directory}/img_{count}.jpg", subimage)
    count += 1
    
