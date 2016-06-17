FROM ubuntu:16.04
MAINTAINER jenkins@toaster.eu
ENTRYPOINT /bin/bash
#
ENV NGINX_VERSION=1.10.0
ENV NGINX_DIR=/src/nginx
# prepare for installation
RUN apt update
RUN apt build-dep nginx -y
RUN apt install git -y
RUN mkdir -p ${NGINX_DIR}
RUN cd ${NGINX_DIR}; apt source nginx -y
RUN cd ${NGINX_DIR}/nginx-${NGINX_VERSION}/debian/modules && \
    git clone https://github.com/wandenberg/nginx-push-stream-module.git --depth=2
RUN cd ${NGINX_DIR}/nginx-${NGINX_VERSION}/debian; \
        sed  -i~ '/add-module=.*nginx-echo/i \\t\t--add-module=$(MODULESDIR)/nginx-push-stream-module \\' rules
COPY ./CHANGELOG /tmp/CHANGELOG
RUN cd ${NGINX_DIR}/nginx-${NGINX_VERSION}/debian; \
        mv changelog changelog.orig; cat /tmp/CHANGELOG changelog.orig > changelog
RUN cd ${NGINX_DIR}/nginx-${NGINX_VERSION}; dpkg-buildpackage -uc -b -j3
