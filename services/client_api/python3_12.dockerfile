FROM ubuntu:22.04

LABEL maintainer="Chukwuma J. Nze"

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE=en_US.UTF-8
ENV TERM xterm

ENV DEBIAN_FRONTEND=noninteractive

ARG XDEBUG_HOST_IP
ARG GIT_USERNAME
ARG GIT_EMAIL

ARG CONTAINER_USER
ARG CONTAINER_UID
ARG CONTAINER_USERGROUP
ARG CONTAINER_GID

RUN apt update                     \
    && apt -y upgrade              \
    && apt-get install -y locales  \
    && locale-gen en_US.UTF-8      \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update                                  \
    && apt-get install -y gnupg tzdata              \
    && echo "UTC" > /etc/timezone                   \
    && dpkg-reconfigure -f noninteractive tzdata    \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confold upgrade -yq \
    && apt-get install -y --allow-downgrades --allow-remove-essential --allow-change-held-packages \
       bash                         \
       build-essential              \
       curl                         \
       gcc                          \
       git                          \
       htop                         \
       llvm                         \
       pkg-config                   \
       software-properties-common   \
       supervisor                   \
       tk-dev                       \
       unzip                        \
       vim                          \
       wget                         \
       xz-utils                     \
       zip                          \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confold upgrade -yq \
    && apt-get install -y --allow-downgrades --allow-remove-essential --allow-change-held-packages \
       libcairo2-dev                \
       libdb5.3-dev                 \
       libexpat1-dev                \
       libffi-dev                   \
       libgdbm-dev                  \
       libgif-dev                   \
       libjpeg-dev                  \
       liblzma-dev                  \
       default-libmysqlclient-dev   \
       libmysqlclient-dev           \
       libncurses5-dev              \
       libncursesw5-dev             \
       libpango1.0-dev              \
       libpcap-dev                  \
       libpq-dev                    \
       libreadline-dev              \
       librsvg2-dev                 \
       libsqlite3-dev               \
       libssl-dev                   \
       libbz2-dev                   \
       zlib1g-dev                   \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/www/json

WORKDIR /var/www/json

COPY ./volumes/repos/client_api .

RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt-get update \
    && apt-get install -y --allow-downgrades --allow-remove-essential --allow-change-held-packages \
       python3.12            \
       python3.12-dev        \
       python3.12-venv       \
       python3-pip           \
       python3.12-distutils  \
       python3-openssl       \
    && rm -rf /var/lib/apt/lists/*


RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 312
RUN update-alternatives --set python3 /usr/bin/python3.12

COPY ./services/client_api/supervisord.conf                  /etc/supervisor/supervisord.conf
COPY ./services/client_api/aliases.bashrc                    /root/aliases.bashrc

RUN cat /root/aliases.bashrc >> /root/.bashrc

RUN git config --global user.name ${GIT_USERNAME}   \
    && git config --global user.email ${GIT_EMAIL}

#RUN set -xe; \
#    groupadd -g 1000 docker_user && \
#    useradd -u 1000 -g docker_user -m docker_user -G docker_env
#RUN echo "docker_user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN python3 -m ensurepip --upgrade  \
    && pip3 install --upgrade pip  \
    && python3 -m pip install --upgrade setuptools  \
    && pip3 install --upgrade setuptools  \
    && pip3 install -r requirements.txt
