FROM phusion/passenger-python312

LABEL maintainer="Chukwuma J. Nze"

RUN apt-get update                  \
    && apt-get install -y locales   \
    && locale-gen en_US.UTF-8

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE=en_US.UTF-8
ENV TERM xterm

ENV DEBIAN_FRONTEND=noninteractive

ARG XDEBUG_HOST_IP
ARG GIT_USERNAME
ARG GIT_EMAIL

RUN apt-get update                                  \
    && apt-get install -y gnupg tzdata              \
    && echo "UTC" > /etc/timezone                   \
    && dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update                      \
    && apt-get -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confold upgrade -yq \
    && apt-get install -y --allow-downgrades --allow-remove-essential --allow-change-held-packages \
       curl                             \
       git                              \
       htop                             \
       supervisor                       \
       unzip                            \
       vim                              \
       zip

RUN mkdir -p /var/www/json

WORKDIR /var/www/json

COPY ./volumes/repos/client_api .

RUN apt-get update \
    && apt-get install -y --allow-downgrades --allow-remove-essential --allow-change-held-packages \
       python3-pip

COPY ./services/client_api/supervisord.conf                  /etc/supervisor/supervisord.conf
COPY ./services/client_api/aliases.bashrc                    /root/aliases.bashrc

RUN cat /root/aliases.bashrc >> /root/.bashrc

RUN git config --global user.name ${GIT_USERNAME}   \
    && git config --global user.email ${GIT_EMAIL}

RUN set -xe; \
    groupadd -g 1000 docker_user && \
    useradd -u 1000 -g docker_user -m docker_user -G docker_env

RUN echo "docker_user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN pip3 install -r requirements.txt
