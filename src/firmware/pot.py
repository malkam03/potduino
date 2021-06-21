# -*- coding: utf-8 -*-


class Pot():
    """The Pot class encapsulates the configuration of each pot

    Args:
        id (int): Identification of the pot.
        rom (str): Address of the DS18X20 temperature sensor.
    """
    def __init__(self, id: int, rom: str) -> None:
        self._temperature_sensor_addr = rom
        self._id = id

    @property
    def id(self) -> int:
        """The ID of the pot
        Return:
            int: the identification of the pot
        """
        return self._id

    @property
    def temperature_sensor_address(self) -> str:
        """Pot DS18X20 temperature sensor address
        Return:
            str: the one wire address of the sensor
        """
        return self._temperature_sensor_addr
