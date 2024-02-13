#!/bin/bash

read -p "Install Pi-radar? [y/N] " response
response=$(echo "$response" | tr '[:upper:]' '[:lower:]')

if [[ "$response" =~ ^(yes|y)$ ]]; then
	echo "Running sudo -v (may require password)..."
	sudo -v
    cd /tmp
    
    echo "Installing pip..."
    curl -Os https://bootstrap.pypa.io/get-pip.py
    sudo python3 get-pip.py
	
    echo "Installing pip-managed dependencies (pyrtlsdr, requests, bs4, pandas)..."
    sudo pip install -q pyrtlsdr requests bs4 pandas
    
    echo "Installing apt-managed dependency (librtlsdr0)..."
    sudo apt install -qqy librtlsdr0
	
	# more here
	
	echo "Installing Pi-radar"
    curl -Os https://codeload.github.com/yellowcress/[URL HERE]/zip/refs/heads/main
    sudo unzip main -d /var/lib/pi-radar

    # more here maybe too
    
    echo "Adding and enabling service..."
    sudo cp /var/lib/pi-radar/pi-radar.service /etc/systemd/system/
    sudo systemctl enable pi-radar.service
    
    echo "Cleaning up..."
    sudo rm /tmp/get-pip.py /tmp/main /
    
    echo "Starting pi-radar..."
    sudo systemctl start pi-radar.service
else
    echo "Pi-radar not installed"
fi