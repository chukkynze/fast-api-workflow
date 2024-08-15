#!/usr/bin/env bash

source ./scripts/makefile/config.sh

read -p "${DEVICE_USER_FIRST_NAME}, are you sure you want to setup the environment up? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    read -p "${DEVICE_USER_FIRST_NAME}? ${DEVICE_USER_FIRST_NAME}? ${DEVICE_USER_FIRST_NAME}? How many times I call your name? This is a destructive. You get backups? " -n 1 -r
    echo    # (optional) move to a new line
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "==============================================="
        printf 'Setting up for %s.\r\n' "${DEVICE_USER_FULL_NAME}"
        echo 'This is DESTRUCTIVE for all your Projects under this environment. So, I hope you have a backup somewhere to be safe.'
        echo '==============================================='
        echo '== Backing up repos'
        echo '==============================================='
        printf '\n'
        # shellcheck disable=SC2046
        cp -a volumes/repos_backup/. volumes/repos_backup_$(date +"%d-%m-%Y_%H-%M-%S")/
        rm -rf volumes/repos_backup/*
        cp -a volumes/repos/. volumes/repos_backup/
        rm -rf volumes/repos/*
        chmod -Rf ugo+rwx volumes/repos_backup

        printf '\n'
        echo '==============================================='
        echo 'Client API setup.'
        echo '==============================================='
        printf '\n'
        mkdir -p volumes/repos/client_api
#        git clone git@bitbucket.org:ogeleiq/client_api.git volumes/repos/client_api/.
#        printf '\n'
#        echo 'Restoring backup git and idea folder if they exist'
#        sudo cp -a volumes/repos_backup/client_api/.git/. volumes/repos/client_api/.git/  || true
#        sudo cp -a volumes/repos_backup/client_api/.idea/. volumes/repos/client_api/.idea/  || true
#        echo 'Creating env files and using potentially existing backup'
#        printf '\n'
#        cp volumes/repos_backup/client_api/.env volumes/repos/client_api/.env  || true
        chown -R "${DEVICE_HOST_USERNAME}":"${DEVICE_HOST_GROUP}" volumes/repos/client_api
        chmod -Rf ugo+rwx volumes/repos/client_api


        printf '\n'
        echo '==============================================='
        echo 'Environment: Fresh Install complete.'
        echo '==============================================='
        echo "${DEVICE_USER_FIRST_NAME}, you can now configure your env variables in .env.docker-compose"
        printf '\n\n'
    fi
fi



