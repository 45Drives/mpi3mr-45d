FROM debian:13

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    linux-headers-amd64 \
    perl \
    python3 \
    libncurses-dev \
    libssl-dev \
    libelf-dev \
    dwarves \
    wget && \
    rm -rf /var/lib/apt/lists/*

COPY docker/entrypoint.sh /entrypoint.sh

VOLUME /src
VOLUME /out

RUN mkdir /build
WORKDIR /build

ENTRYPOINT [ "/entrypoint.sh" ]

COPY docker/proxmox.sources /etc/apt/sources.list.d/

RUN sed -i 's/^Suites:.*/Suites: trixie/' /etc/apt/sources.list.d/proxmox.sources

RUN wget https://enterprise.proxmox.com/debian/proxmox-archive-keyring-trixie.gpg -O /usr/share/keyrings/proxmox-archive-keyring.gpg && \
    apt-get -y update && \
    apt-get install -y pve-headers && \
    rm -rf /var/lib/apt/lists/*
