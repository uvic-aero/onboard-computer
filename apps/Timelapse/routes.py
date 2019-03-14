from apps.Timelapse.handlers import Status, Stop, Start, SetInterval, SetDuration

routes = [
    (r"/status/timelapse", Status),
    (r"/start/timelapse", Start),
    (r"/stop/timelapse", Stop),
    (r"/setInterval/timelapse", SetInterval),
    (r"/setDuration/timelapse", SetDuration),
]
