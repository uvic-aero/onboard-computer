from apps.Pixhawk.handlers import Status, Stop, Start

routes = [
    (r"/status/pixhawk", Status),
    (r"/start/pixhawk", Start),
    (r"/stop/pixhawk", Stop),
]
