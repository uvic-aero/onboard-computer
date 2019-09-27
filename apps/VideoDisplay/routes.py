from apps.VideoDisplay.handlers import Status, Stop, Start

routes = [
    (r"/status/videoDisplay", Status),
    (r"/start/videoDisplay", Start),
    (r"/stop/videoDisplay", Stop),
]
