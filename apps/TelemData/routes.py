from apps.TelemData.handlers import Status, Stop, Start 

routes = [
    (r"/status/telemData", Status),
    (r"/start/telemData", Start),
    (r"/stop/telemData", Stop),
]
