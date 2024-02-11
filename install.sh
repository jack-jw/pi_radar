#!/bin/bash

read -p "Install Pi-radar? [y/N] " response
response=$(echo "$response" | tr '[:upper:]' '[:lower:]')

if [[ "$response" =~ ^(yes|y)$ ]]; then
	echo "Running sudo -v (may require password)"
	sudo -v
	cd /var/lib/
	echo "Cloning github.com/yellowcress/pi-radar..."
    sudo git clone https://github.com/yellowcress/pi-radar.git
    
    echo "Installing dependencies"
    sudo apt install -y python3-requests
    sudo apt install -y python3-bs4
    sudo apt install -y python3-pandas
    
    
    # add dump1090, gfx-hat config etc here
    
    echo "Adding and enabling service..."
    sudo cp /opt/pi-radar/pi-radar.service /etc/systemd/system/
    sudo systemctl enable pi-radar.service
    echo "Starting pi-radar..."
    sudo systemctl start pi-radar.service
else
    echo "Pi-radar not installed"
fi