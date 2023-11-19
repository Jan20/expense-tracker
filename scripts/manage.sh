#!/usr/bin/env bash
case ${1} in
start)
    echo "Starting the postgres database"
    cd ../docker
    docker-compose -f docker-compose.yml up -d
;;
stop)
    echo "Starting the postgres database"
    cd ../docker
    docker-compose down
;;
esac
