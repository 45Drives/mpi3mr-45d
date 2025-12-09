FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        linux-headers-generic \
        make \
        gcc \
        perl \
        python3 \
        libncurses-dev \
        libssl-dev \
        libelf-dev \
        dwarves && \
    rm -rf /var/lib/apt/lists/*

COPY docker/entrypoint.sh /entrypoint.sh

VOLUME /src
VOLUME /out

RUN mkdir /build
WORKDIR /build

ENTRYPOINT [ "/entrypoint.sh" ]
