FROM rockylinux:9-minimal

RUN microdnf -y install dnf dnf-plugins-core && \
    dnf -y groupinstall 'Development Tools' && \
    dnf -y install kernel-devel make gcc perl ncurses-devel openssl-devel elfutils-libelf-devel python3 && \
    dnf config-manager --set-enabled crb && \
    dnf -y install dwarves && \
    dnf clean all && \
    rm -rf /var/cache/dnf

COPY docker/entrypoint.sh /entrypoint.sh

VOLUME /src
VOLUME /out
RUN mkdir /build
WORKDIR /build

ENTRYPOINT [ "/entrypoint.sh" ]
