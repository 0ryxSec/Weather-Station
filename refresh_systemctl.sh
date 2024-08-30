#!/bin/bash

# Stop the new service if it's running
sudo systemctl stop weather-station.service

# Disable the new service
sudo systemctl disable weather-station.service

# Remove the new service file if it exists
sudo rm /etc/systemd/system/weather-station.service

# Create the new service file
sudo bash -c 'cat << EOF > /etc/systemd/system/weather-station.service
[Unit]
Description=Weather Station Data Logger

[Service]
ExecStart=/usr/bin/python3 /home/[USER]/weather/weather-station.py
WorkingDirectory=/home/[USER]/weather
StandardOutput=inherit
StandardError=inherit
Restart=always
User=[USER]

[Install]
WantedBy=multi-user.target
EOF'

# Reload the systemd configuration
sudo systemctl daemon-reload

# Enable the new service
sudo systemctl enable weather-station.service

# Start the new service
sudo systemctl start weather-station.service

# Check the status of the new service
sudo systemctl status weather-station.service
