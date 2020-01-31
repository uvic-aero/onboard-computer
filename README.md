# UVic AERO Onboard Computer

The purpose of the Onboard Computer (OBC) is to provide an functionality and interfacing to remote vehicles. The software runnning on OBC will adapt with the requirements of each years competition.

### Requirements
* Python3.6 or greater

### Getting Started
1. Install python3.6 or greater
1. Clone repository `git clone https://github.com/uvic-aero/onboard-computer.git`
1. Change directory into onboard computer `cd onboard-computer`
1. Create Python3 virtual env `python3 -m venv env`
1. Activate virtual environment `source env/bin/activate` 
1. Install python requirements `pip3 install -r requirements.txt`

### Configuration 
1. Open the `config.ini` file located in the root directory of this repository
1. Edit the groundstation ip address to http://[address of machine runnig gcs]
1. Leave groundstation port as is unless explicitly modified on gcs

### Running 
Start obc by running (in the repository root)
	`python3 obc.py`
	
Check that the software is running by visiting the server
  [http://0.0.0.0:1600/status/piCam](http://0.0.0.0:1600/status/piCam)

## Running Unittests

Tests live in the `/test` directory and can be ran with `python3 -m unittest test.[test_module_name]`

For example run the Vision test with:
`python3 -m unittest test.test_vision`

<!--
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

Christopher Hampu, Lin Hsuan-Yu, TaeHun Kang

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
-->
