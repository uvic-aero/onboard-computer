#!/bin/bash

echo "Installing basic system tools..."
sudo apt update
sudo apt upgrade -y
sudo apt install python3 -y
sudo apt install python3-pip -y
sudo apt install vim -y

echo "Installing OBC Python requirements..."
sudo pip3 install -r requirements.txt

echo "Calling OpenCV install script..."
sudo bash OpenCV-4-RPi-Install.sh

echo "Add OBC service daemon..."
if [ "$#" -ne 1 ]; then
    echo "Using current directory as install directory"
    path=$(pwd)
else
    path=$1
fi
sed -i -e "s@dir@${path}@g" ./obc.service
sudo cp obc.service /etc/systemd/system
sudo systemctl start obc.service
sudo systemctl enable obc.service
sudo systemctl daemon-reload

echo "Raspberry Pi setup complete."
