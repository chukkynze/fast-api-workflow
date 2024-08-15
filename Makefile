include .env.docker-compose

# Core Commands
###########################

# Runs before every command to get the most recent configs
get_configs:
	cp -a .env.docker-compose ./scripts/makefile/config.sh

setup: get_configs
	./scripts/makefile/setup.sh



# Docker Commands
####################################################
clean: status
	./scripts/makefile/clean_docker_all.sh

boot: get_configs
	./scripts/makefile/boot.sh

boot_bg: get_configs
	./scripts/makefile/boot.sh silent

boot_clean: clean boot

boot_bg_clean: clean boot_bg

status: get_configs
	./scripts/makefile/status.sh



# Access Commands
####################################################
client_api_ssh:
	@echo 'SSH into the client_api container at /var/www/json'
	docker exec -it -w /var/www/json client_api bash

