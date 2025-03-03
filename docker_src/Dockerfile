FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    build-essential cmake git \
    libboost-all-dev libssl-dev \
    libzmq3-dev pkg-config \
    python3 python3-pip \
    python3-setuptools python3-wheel \
    wget libdcmtk-dev libdlib-dev libfftw3-dev \
    libinsighttoolkit5-dev \
    libpng-dev libtiff-dev uuid-dev zlib1g-dev \
    plastimatch && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# RUN apt-get install pipx
RUN pip3 install --break-system-packages pyplastimatch
# RUN python3 -c 'from pyplastimatch.utils.install import install_precompiled_binaries; install_precompiled_binaries()'

# ENTRYPOINT ["plastimatch"]

