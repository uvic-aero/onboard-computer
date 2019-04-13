class Telemetry:
    def __init__(self):
        self.lat = 49
        self.lng = -123

    # Start the timelapse application     
    def start(self):
        pass
    
    # Stop the timelapse application 
    def stop(self):
        pass 

    def get_coord(self):
        return { 'lat': 49.121312, 'lng': -123.123121 }

telemetry = Telemetry()
