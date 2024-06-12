#!/usr/bin/env bash
case ${1} in
start)
    echo "Starting the postgres database"
    echo $POSTGRES_DATABASE_PORT
    cd ../docker
    docker-compose --env-file ../.env -f docker-compose.yml up -d
;;
stop)
    echo "Starting the postgres database"
    cd ../docker
    docker-compose down
;;
esac
