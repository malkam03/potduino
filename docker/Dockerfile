FROM python:3

# REPL
RUN apt-get update && \
    apt-get install -y picocom && \
    rm -rf /var/lib/ap/lists/*

ARG USER=dev
ARG USERID=1000
ARG DIALOUTGID
RUN useradd -ms /bin/bash ${USER} -u ${USERID} && \
    if [ ! -z ${DIALOUTGID} ]; then \
        groupmod -n dialout-old dialout && \
        groupadd -g ${DIALOUTGID} dialout; \
    fi && \
    usermod -aG dialout ${USER}

USER ${USER}

# Python tools
ENV PATH="$PATH:/home/${USER}/.local/bin/"
RUN pip install -U \
    esptool \
    adafruit-ampy \
    sphinx \
    myst-parser

# Dev Aliases
RUN echo "alias mcls='ampy --port \$UART_DEV --baud 115200 ls'\n \
    alias mcrm='ampy --port \$UART_DEV --baud 115200 rm'\n \
    alias mcget='ampy --port \$UART_DEV --baud 115200 get'\n \
    alias mcput='ampy --port \$UART_DEV --baud 115200 put'\n \
    alias mcget='ampy --port \$UART_DEV --baud 115200 get'\n \
    alias mcrun='ampy --port \$UART_DEV --baud 115200 run'\n \
    alias mcflashclean='esptool.py --port \$UART_DEV erase_flash'\n \
    alias mcflash='esptool.py --port \$UART_DEV --baud 460800 write_flash --flash_size=detect 0'\n \
    alias mccon='picocom \$UART_DEV -b115200'" >> ~/.bashrc

VOLUME /tmp/potduino

WORKDIR /tmp/potduino

ENTRYPOINT [ "bash" ]
