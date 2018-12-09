#   import app GET responses
from apps.Timelapse.routes import routes as tRoutes
from apps.ImageService.routes import routes as isRoutes
from apps.VideoDisplay.routes import routes as vdRoutes


routes = tRoutes + isRoutes + vdRoutes
