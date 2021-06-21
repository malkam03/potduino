# -*- coding: utf-8 -*-
"""
Main module, it's executed automatically after
the boot.py

Instantiates the potduino, perform the actions (
log_sensor_data
) and then sleeps for a period of time only to
start again
"""

import ntptime  # noqa: E0401
from pot import Pot

from potduino import Potduino


def main():
    ntptime.settime()
    potduino = Potduino(sleep_minutes=1)
    for id, rom in enumerate(potduino._roms):
        pot = Pot(id, str(rom))
        potduino.add_pot(pot)

    potduino.log_sensor_data()
    potduino.sleep()


if __name__ == '__main__':
    main()
