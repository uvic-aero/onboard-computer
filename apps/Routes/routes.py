#   import app GET responses
from apps.ImageService.imageService import ImageServiceStatus, ImageServiceStart, ImageServiceStop
from apps.Timelapse.timelapse import TimelapseStatus, TimelapseStart, TimelapseStop, TimelapseSetInterval
from apps.VideoDisplay.videoDisplay import VideoDisplayStatus, VideoDisplayStart, VideoDisplayStop

routes = [
    (r"/status/imageService", ImageServiceStatus),
    (r"/status/timelapse", TimelapseStatus),
    (r"/status/videoDisplay", VideoDisplayStatus),
    (r"/start/imageService", ImageServiceStart),
    (r"/start/timelapse", TimelapseStart),
    (r"/start/videoDisplay", VideoDisplayStart),
    (r"/stop/imageService", ImageServiceStop),
    (r"/stop/timelapse", TimelapseStop),
    (r"/stop/videoDisplay", VideoDisplayStop),
    (r"/setInterval/timelapse", TimelapseSetInterval),
]

