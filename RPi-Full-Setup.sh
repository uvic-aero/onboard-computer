#!/bin/bash

echo "Installing basic system tools..."
sudo apt update
sudo apt upgrade -y
sudo apt install python3 -y
sudo apt install python3-pip -y
sudo apt install vim -y
echo "Done!"

echo "Installing OBC Python requirements..."
sudo pip3 install -r requirements.txt
echo "Done!"

echo "Calling OpenCV install script..."
sudo bash OpenCV-4-RPi-Install.sh

echo "Raspberry Pi setup complete."
