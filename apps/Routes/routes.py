#   import app GET responses
from apps.ImageService.imageService import ImageServiceStatus, ImageServiceStart, ImageServiceStop
from apps.VideoDisplay.videoDisplay import VideoDisplayStatus, VideoDisplayStart, VideoDisplayStop
from apps.Timelapse.routes import routes as tlRoutes

routes = tlRoutes
