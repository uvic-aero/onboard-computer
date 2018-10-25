
# Create an async HTTP Client that can take in images and send them to the GroundStation
class ImageService:
    
    def __init__(self):
        pass

# Export a singleton accessible from camera/liveview classes
image_service = ImageService()
