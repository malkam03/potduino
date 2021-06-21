# -*- coding: utf-8 -*-

import logging
import time

import ahtx0  # noqa: E0401
import machine  # noqa: E0401
from bh1750 import BH1750  # noqa: E0401
from ds18x20 import DS18X20  # noqa: E0401
from machine import I2C, Pin  # noqa: E0401
from onewire import OneWire  # noqa: E0401
from pot import Pot


class Potduino():
    """The potduino class encapsulates the hardware functionality

    Args:
        scl_pin (int): I2C Clock pin in which the ATH10 and BH1750 are
                       connected to, default 5.
        sda_pin (int): I2C Data pin in which the ATH10 and BH1750 are
                       connected to, default 4.
        ds_pin (int): OneWire Data pin in which the BH1750 sensors are
                       connected to, default 14.
        sleep_minutes (int): minutes in which the device will be in deep
                             sleep between operations.
    """
    def __init__(self,
                 scl_pin: int = 5,
                 sda_pin: int = 4,
                 ds_pin: int = 14,
                 sleep_minutes: int = 60) -> None:
        self._i2c = I2C(scl=Pin(scl_pin), sda=Pin(sda_pin))
        self._ambient_sensor = ahtx0.AHT10(self._i2c)
        self._luminosity_sensor = BH1750(self._i2c)

        self._ds_sensors = DS18X20(OneWire(Pin(ds_pin)))
        self._roms = self._ds_sensors.scan()
        self._sleep_time = int(sleep_minutes * 1e3 * 60)
        self._pots: list(Pot) = []

    def add_pot(self, pot: Pot) -> None:
        """Add a pot configuration to the device

        Args:
            pot (Pot): pot object with the settings specific to that pot
        """
        self._pots.append(pot)

    def log_sensor_data(self, log_file: str = "sensor_data.log") -> None:
        """Writes the sensor data into the `file_name` with timestamp

        Args:
            log_file (str): path to the logging file
        """
        logging.basicConfig(level=logging.INFO,
                            filename=log_file,
                            format='%(asctime)s;%(message)s')

        sensor_data = self.get_sensors_data()
        logging.info(str(sensor_data))

    def get_sensors_data(self) -> "dict[str, int]":
        """Return a dictionary with a sensor ID and the retrieved value

        Note:
            IDS:
                AL: Ambient Light Sensor
                AH: Ambient Humidity Sensor
                AT: Ambient Temperature Sensor
                TXX: Pot Soil temperature Sensor (XX is a two digit ID for the
                pot)

        Returns:
            dict{str,int}: a dict with the sensor iD and the retrieved value
        """
        light = self._luminosity_sensor.luminance(BH1750.ONCE_HIRES_2)
        temp = self._ambient_sensor.temperature
        hum = self._ambient_sensor.relative_humidity
        sensor_data = {"AL": light, "AH": hum, "AT": temp}
        pot_temperatures = self._pots_temperature()
        for pot in self._pots:
            sensor_data["T{:0>2d}".format(
                pot.id)] = pot_temperatures[pot.temperature_sensor_address]

        return sensor_data

    def _pots_temperature(self) -> "dict[str, int]":
        """Get temperatures from the DS18X20 sensors
        Returns:
            dict{str: int}: a dict with the sensor one wire address and
                               the temperature
        """
        self._ds_sensors.convert_temp()
        time.sleep_ms(750)
        return {
            str(rom): self._ds_sensors.read_temp(rom)
            for rom in self._roms
        }

    def sleep(self):
        """Puts the device in deep sleep mode for the predefined time
        """
        rtc = machine.RTC()
        rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
        rtc.alarm(rtc.ALARM0, self._sleep_time)
        machine.deepsleep()
