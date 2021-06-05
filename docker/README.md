# Potduino Dev Docker

Contains the dependencies required to flash/develop for potduino project.

## Getting Started

### Prerequisities

In order to build/run this dockerfile you'll need to install docker. See installation instructions at [Getting started with docker in Linux](https://docs.docker.com/linux/started/).

### Usage

You can interactively run this container from a terminal with the following commands:

```shell
$ export UART_DEV=/dev/ttyUSB0
$ docker run -ti --rm -v $(pwd):/tmp/potduino -e UART_DEV --device=$UART_DEV potduino-dev
```

**Note**: Remember to update the `UART_DEV` variable with the correct uart device. You can disconnect the device, list the files and then connect the device and list the devices again. This way the latest connected uart dev should be the one you'll want to work with.

#### Aliases

This dockerfile populate the following aliases to make it easier to remember the commands to interact with the device.

- **mcls**: ampy --port \$UART_DEV --baud 115200 ls
- **mcrm**: ampy --port \$UART_DEV --baud 115200 rm
- **mcget**: ampy --port \$UART_DEV --baud 115200 get
- **mcput**: ampy --port \$UART_DEV --baud 115200 put
- **mcget**: ampy --port \$UART_DEV --baud 115200 get
- **mcrun**: ampy --port \$UART_DEV --baud 115200 run
- **mcflashclean**: esptool.py --port \$UART_DEV erase_flash
- **mcflash**: esptool.py --port \$UART_DEV --baud 460800 write_flash --flash_size=detect 0
- **mccon**: picocom \$UART_DEV -b115200

#### Volumes

- `/tmp/potduino` - The contents of this repo are expected to be mounted in this path

## Building

In order to build the image just type on a terminal:

```shell
$ docker build --build-arg USER=$USER --build-arg USERID=$UID --build -t potduino-dev -f docker/Dockerfile .
```

And, if the id of the dialout group is different than 20, you can also pass `DIALOUTGID`:

```shell
$ docker build --build-arg USER=$USER --build-arg USERID=$UID --build-arg DIALOUTGID=<gid> --build -t potduino-dev -f docker/Dockerfile .
```

## Contributing

Please read [CONTRIBUTING.md](../CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](../LICENSE) file for details.
