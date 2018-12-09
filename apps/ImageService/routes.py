from apps.ImageService.handlers import Status, Stop, Start, SetInterval 

routes = [
    (r"/status/imageService", Status),
    (r"/start/imageService", Start),
    (r"/stop/imageService", Stop),
]
