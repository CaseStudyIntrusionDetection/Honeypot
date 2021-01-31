#!/bin/sh

echo "Tanner (and Sandboxes):"
cd tanner
docker-compose up -d $@

echo "Website target:"
cd ../target
docker-compose up -d

echo "Snare:"
cd ../snare
docker-compose up -d $@
