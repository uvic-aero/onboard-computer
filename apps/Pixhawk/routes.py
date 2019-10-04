from apps.Pixhawk.handlers import Status, Stop, Start 

routes = [
    (r"/status/telemData", Status),
    (r"/start/telemData", Start),
    (r"/stop/telemData", Stop),
]
