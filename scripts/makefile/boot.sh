#!/usr/bin/env bash

source ./scripts/makefile/config.sh

if [[ "$1" == "silent" ]]; then
  echo "Bring Up Docker Environment Silently."
else
  echo "Bring Up Docker Environment."
fi

# MySQL setup
chmod 0444 ./volumes/data/emp/mysql/config/mysql.cnf

docker-compose version
docker-compose --env-file="$DEFAULT_DOCKER_COMPOSE_ENV_FILE" config

if [[ "$1" == "silent" ]]; then
  docker-compose --env-file="$DEFAULT_DOCKER_COMPOSE_ENV_FILE" up --force-recreate -d --watch
else
  docker-compose --env-file="$DEFAULT_DOCKER_COMPOSE_ENV_FILE" up --force-recreate --watch
fi