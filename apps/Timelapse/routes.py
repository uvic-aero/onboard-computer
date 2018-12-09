from apps.Timelapse.handlers import Status, Stop, Start, SetInterval 

routes = [
    (r"/status/timelapse", Status),
    (r"/start/timelapse", Start),
    (r"/stop/timelapse", Stop),
    (r"/setInterval/timelapse", SetInterval),
]


