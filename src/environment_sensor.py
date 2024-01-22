from typing import Protocol
from dataclasses import dataclass
import logging
from adafruit_scd4x import SCD4X
import adafruit_si7021
import asyncio

@dataclass
class Reading:
    measurement_type: str
    value: float
    unit: str


def get_environment_sensor(i2c):
    logger = logging.getLogger("EnvironmentSensor")
    logger.debug("Scanning I2C bus")
    while not i2c.try_lock():
        logger.debug("I2C bus locked, waiting")
        pass
    
    try:
        for device_address in i2c.scan():
            logger.debug("Found device at 0x%x", device_address)
            if device_address == 0x40:
                logger.debug("Found Si7021")
                i2c.unlock()
                return Si7021EnvironmentSensor(i2c)
            if device_address == 0x62:
                logger.debug("Found SCD4X")
                i2c.unlock()
                return SCD40EnvironmentSensor(i2c)
            
    except Exception as e:
        logger.error("Error scanning I2C bus: %s")
    finally:
        logger.debug("Unlocking I2C bus in finally block")
        i2c.unlock()

def convert_c_to_f(c):
    return c * 9 / 5 + 32


class EnvironmentSensor(Protocol):

    def get_new_readings(self):
        '''Returns the temperature in degrees Celsius'''

    def start_readings(self):
        '''Starts the sensor taking readings'''

class SCD40EnvironmentSensor(EnvironmentSensor):
    
    def __init__(self, i2c):
        self.logger = logging.getLogger("SCD4X")
        self.logger.debug("Initializing SCD4X")
        self._scd4x = SCD4X(i2c)
        self.logger.debug("SCD4X initialized")
        

    def start_readings(self):
        self._scd4x.start_periodic_measurement()


    def get_new_readings(self):
        if self._scd4x.data_ready:
            return [
                Reading("carbon_dioxide", self._scd4x.CO2, "ppm"),
                Reading("temperature", convert_c_to_f(self._scd4x.temperature), "F"),
                Reading("humidity", self._scd4x.relative_humidity, "%"),
            ]
        return []

class Si7021EnvironmentSensor(EnvironmentSensor):
    
    def __init__(self, i2c):
        self.logger = logging.getLogger("Si7021")
        self.logger.debug("Initializing Si7021")
        self._si7021 = adafruit_si7021.SI7021(i2c)
        self.logger.debug("Si7021 initialized")
        

    def start_readings(self):
        pass


    def get_new_readings(self):
        return [
            Reading("temperature", convert_c_to_f(self._si7021.temperature), "F"),
            Reading("humidity", self._si7021.relative_humidity, "%"),
        ]

def sensor_task_setup(sensor):
    sensor.start_readings()

async def sensor_task_loop(thermostat, sensor):
    readings = sensor.get_new_readings()
    thermostat.handle_new_readings(readings)
    await asyncio.sleep(5)

async def sensor_task(thermostat, sensor):
    logger = logging.getLogger("Environment Sensor Task")
    logger.info("Starting environment sensor task")
    while True:
        logger.debug("Getting new readings")
        await sensor_task_loop(thermostat, sensor)
        