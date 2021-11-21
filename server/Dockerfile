FROM ubuntu:focal
ENV PYTHONBUFFERED=1 LANG=C.UTF-8 LANGUAGE=C.UTF-8 LC_ALL=C.UTF-8 DEBIAN_FRONTEND=noninteractive
ARG PIPENVDEV=--dev
WORKDIR /app/server
COPY package_install package_dist_upgrade /usr/sbin/
RUN chmod 755 /usr/sbin/package_install /usr/sbin/package_dist_upgrade && \
    package_dist_upgrade && \
    package_install python3 python3-distutils python3-setuptools python3-wheel curl ca-certificates apt-transport-https && \
    curl https://bootstrap.pypa.io/get-pip.py | python3 - && \
    ln -sf /usr/bin/pip3 /usr/bin/pip && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    pip install pdm
ENTRYPOINT [ "pdm", "run"]
ADD pyproject.toml pdm.lock /app/server/
RUN pdm sync
ADD . /app/server/