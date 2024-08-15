#!/usr/bin/env bash

source ./scripts/makefile/config.sh

# shellcheck disable=SC2046
printf "\n"
printf "============================================ \n"
printf "Docker Environment Status \n"
printf "============================================ \n"
printf "\n"
printf "Docker Volumes \n"
printf "============================================ \n"
docker volume ls || true
printf "\n"
printf "Docker Images \n"
printf "============================================ \n"
docker images -a || true
printf "\n"
printf "Docker Stats \n"
printf "============================================ \n"
docker ps -a || true
printf "\n"
printf "Docker Compose Stats \n"
printf "============================================ \n"
docker-compose --env-file="$DEFAULT_DOCKER_COMPOSE_ENV_FILE" ps || true
printf "\n"
printf "Docker Stats: System & Hard drive \n"
printf "============================================ \n"
docker system df || true
printf "\n"
printf "Docker Stats: CPU, Mem, Bandwidth \n"
printf "============================================ \n"
# shellcheck disable=SC2046
docker stats --no-stream $(docker ps | awk '{if(NR>1) print $NF}') || true
printf "\n"
printf "Docker IPs: \n"
printf "============================================ \n"
# shellcheck disable=SC2046
docker inspect -f '{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -aq) || true