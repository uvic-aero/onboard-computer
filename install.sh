#!/bin/bash
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