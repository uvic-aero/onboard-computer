# UVic AERO Onboard Computer

The purpose of the Onboard Computer (OBC) is to remotely control our camera (Sony ILCE 5100), utilize the camera API, and stream images/video from the camera to our ground station

## Getting Started

The following instructions will help you get the project running

### Prerequisites

This project is dependent on Python 3.6+ and requires installing a few dependencies

### Installing

First ensure that Python 3.6+ and Python-Pip are installed

Next install the project dependencies

```
pip install -r requirements.txt
```

Then run the project while the camera is turned on

```
python obc.py
```

The project will begin searching for the camera and will attempt to connect to it and control it
This requires having a Wi-Fi connection to the camera hotspot

## Livestreaming video

The jpeg livestream will be served on http://127.0.0.1:5000 but is meant to be dijested by ffmpeg/ffserver

### Set up livestreaming on Linux

First ensure that ffmpeg is installed on your system

```
apt-get install ffmpeg
```

Then use the ffserver config to start the program

```
ffserver -f ffserver.conf
```

Next you will run the OBC and wait for the image livestream to start

```
python obc.py
```

Then start ffmpeg to transcode the images into a video stream

```
ffmpeg -c mjpeg -i http://127.0.0.1:5000 -codec copy http://127.0.0.1:8080/feed1.ffm
```

The video livestream can now be viewed at http://127.0.0.1:8080/liveview.jpg depending on how ffserver is configured
The local IP in the link above can be replaced by the IP of the server/raspberry Pi depending how the network is configured as
ffserver will run on all network interfaces whereas the initial jpeg stream will only run locally.

## Authors

Christopher Hampu, Lin Hsuan-Yu

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
