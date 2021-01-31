#!/bin/sh

echo "Snare:"
cd ./snare
docker-compose stop 

echo "Website target:"
cd ../target
docker-compose stop

echo "Tanner (and Sandboxes):"
cd ../tanner
docker-compose stop 
