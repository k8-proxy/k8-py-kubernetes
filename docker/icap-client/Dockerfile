FROM gcc:latest

RUN apt update -y && apt-get install -y \
    curl \
    make \
    libtool \
    automake \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/filetrust/c-icap.git /src
WORKDIR /src/c-icap
RUN autoreconf -ivf \
    && ./configure --prefix=/usr/local/c-icap \
    && make; make install

ENTRYPOINT [ "/usr/local/c-icap/bin/c-icap-client" ]
