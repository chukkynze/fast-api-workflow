#!/usr/bin/env bash

source ./scripts/makefile/config.sh

echo "Container cleaning started..."
# shellcheck disable=SC2046
docker rm $(docker ps -aq) -f
docker ps -a

echo "Image cleaning started..."
# shellcheck disable=SC2046
docker rmi $(docker images -aq) -f
docker images -a

echo "Complete clean started..."
docker-compose --env-file="${DEFAULT_DOCKER_COMPOSE_ENV_FILE}" down \
&& docker system prune -f \
&& docker volume prune -f \
&& docker ps -a \
&& docker-compose --env-file="${DEFAULT_DOCKER_COMPOSE_ENV_FILE}" ps

echo 'Clean: Client MySQL'
sudo chown -R "${DEVICE_HOST_USERNAME}":"${DEVICE_HOST_GROUP}" volumes/data/client/mysql/storage/persist
rm -Rf volumes/data/client/mysql/storage/persist/*

echo 'Clean: Client PostgresSQL'
sudo chown -R "${DEVICE_HOST_USERNAME}":"${DEVICE_HOST_GROUP}" volumes/data/client/postgres/storage/persist
rm -Rf volumes/data/client/postgres/storage/persist/*