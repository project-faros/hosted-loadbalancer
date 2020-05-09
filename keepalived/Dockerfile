FROM registry.access.redhat.com/ubi8/ubi-minimal:latest
LABEL maintainer="Ryan Kraus (rkraus@redhat.com)"

COPY requirements.txt /requirements.txt
RUN microdnf update

RUN microdnf install iproute wget hostname tar gzip python3 keepalived nc; \
    pip3 install -r requirements.txt; \
    # cd /usr/local/bin; \
    # wget -O oc.tgz https://mirror.openshift.com/pub/openshift-v4/clients/oc/latest/linux/oc.tar.gz; \
    # tar xvzf oc.tgz; \
    rm -rf /var/cache/yum;

WORKDIR /app
COPY app /app
CMD /app/init.py
