from apps.PiCam.handlers import Status, TakePicture, StartVideo, StopVideo, StartPreview, StopPreview, GetExposureCompensation, SetExposureCompensation, IncExposureCompensation, DecExposureCompensation, GetShutterSpeed, SetShutterSpeed, IncShutterSpeed, DecShutterSpeed, GetAwbMode, SetAwbMode, GetAwbGains, SetAwbGains, IncAwbGains, DecAwbGains, GetIso, SetIso, IncIso, DecIso 

routes = [
    (r"/status/piCam", Status),
    (r"/takePicture", TakePicture),
    (r"/startVideo/piCam", StartVideo),
    (r"/stopVideo/piCam", StopVideo),
    (r"/startPreview/piCam", StartPreview),
    (r"/stopPreview/piCam", StopPreview),
    (r"/getExposureCompensation/piCam", GetExposureCompensation),
    (r"/setExposureCompensation/piCam", SetExposureCompensation),
    (r"/incExposureCompensation/piCam", IncExposureCompensation),
    (r"/decExposureCompensation/piCam", DecExposureCompensation),
    (r"/getShutterSpeed/piCam", GetShutterSpeed),
    (r"/setShutterSpeed/piCam", SetShutterSpeed),
    (r"/incShutterSpeed/piCam", IncShutterSpeed),
    (r"/decShutterSpeed/piCam", DecShutterSpeed),
    (r"/getAwbMode/piCam", GetAwbMode),
    (r"/setAwbMode/piCam", SetAwbMode),
    (r"/getAwbGains/piCam", GetAwbGains),
    (r"/setAwbGains/piCam", SetAwbGains),
    (r"/incAwbGains/piCam", IncAwbGains),
    (r"/decAwbGains/piCam", DecAwbGains),
    (r"/getIso/piCam", GetIso),
    (r"/setIso/piCam", SetIso),
    (r"/incIso/piCam", IncIso),
    (r"/decIso/piCam", DecIso)
]
