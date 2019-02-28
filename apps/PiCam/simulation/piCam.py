class PiCam:
    def __init__(self):
        self.now = datetime.datetime.now()
        self.status = 'unset status'
   
    def take_picture(self):
        print('Camera Simulating Image Capture')

# Export singleton
piCam = PiCam()

