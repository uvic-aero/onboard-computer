from apps.ImageService.handlers import Status, Stop, Start

routes = [
    (r"/status/imageService", Status),
    (r"/start/imageService", Start),
    (r"/stop/imageService", Stop),
]
