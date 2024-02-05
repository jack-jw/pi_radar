#!/bin/bash

read -p "Install Pi-radar? [y/N] " response
response=$(echo "$response" | tr '[:upper:]' '[:lower:]')

if [[ "$response" =~ ^(yes|y)$ ]]; then
    # installer script
else
    echo "Pi-radar not installed"
fi