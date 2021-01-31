#!/bin/sh
if [ $# = "1" ]; then
	if [ $1 = "b" ]; then
		docker-compose -f docker-compose.dev.yml build 
	fi;
fi;

docker-compose -f docker-compose.dev.yml run --service-ports snare-dev 