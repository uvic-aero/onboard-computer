#import singleton instance of apps 
from apps.ImageService.imageService import imageService, ImageServiceStatus, ImageServiceStart, ImageServiceStop
from apps.Timelapse.timelapse import timelapse, TimelapseStatus, TimelapseStart, TimelapseStop
from apps.VideoDisplay.videoDisplay import videoDisplay, VideoDisplayStatus, VideoDisplayStart, VideoDisplayStop

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
]

