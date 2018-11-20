#!/bin/bash
cp obc.service /etc/systemd/system
sudo systemctl start obc.service
sudo systemctl enable obc.service