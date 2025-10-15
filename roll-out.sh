#!/bin/bash

# This script automates the update and deployment of a discord bot

kill $(pgrep -f 'main.py')
git pull origin main
python3 src/main.py &
echo "Bot updated and restarted."