from ubuntu:22.04

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libboost-all-dev \
    libssl-dev \
    libzmq3-dev \
    pkg-config \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir numpy SimpleITK pandas requests

RUN pip install git+https://github.com/AIM-Harvard/pyplastimatch.git@bin
RUN python3 -c 'from pyplastimatch.utils.install import install_compiled_binaries; install_compiled_binaries()'

ENTRYPOINT ["plastimatch"]

