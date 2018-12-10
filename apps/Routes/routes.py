# import routes from each application
from apps.Timelapse.routes import routes as tRoutes
from apps.ImageService.routes import routes as isRoutes
from apps.VideoDisplay.routes import routes as vdRoutes

# Concatonate all available routes
routes = tRoutes + isRoutes + vdRoutes
