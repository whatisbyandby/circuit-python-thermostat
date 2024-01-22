import logging
import asyncio
from enum import Enum
from dataclasses import dataclass

@dataclass
class ThermostatState:
    current_temperature: float
    target_temperature: float
    current_humidity: float
    fan_mode: str
    mode: str


class ThermostatMode(str, Enum):
    OFF = "off"
    HEAT = "heat"
    COOL = "cool"
    AUTO = "auto"
    FAN_ONLY = "fan_only"

class FanMode(str, Enum):
    AUTO = "auto"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TemperatureUnits(str, Enum):
    F = "F"
    C = "C"


class Thermostat:
    def __init__(self, device_id, state_queue):
        self.device_id = device_id
        self.logger = logging.getLogger("Thermostat")
        self._state_queue = state_queue
        self._current_temperature = None
        self._target_temperature = None
        self._current_humidity = None
        self._mode = ThermostatMode.HEAT
        self._fan_mode = FanMode.AUTO
        self._units = TemperatureUnits.F
        self._room = "living room"


    def initalize(self):
        self.logger.debug("Initializing Thermostat")
        self.environment_sensor.start_readings()

    def _publish_state(self):
        state = self.get_state()
        self.logger.debug(f"Publishing state: {state}")
        self._state_queue.put_nowait(state)

    def handle_new_readings(self, readings):
        for reading in readings:
            if reading.measurement_type == "temperature":
                self._current_temperature = reading.value
            if reading.measurement_type == "humidity":
                self._current_humidity = reading.value
        self._publish_state()
        
    def handle_command(self, command):
        self.logger.debug(f"Got command: {command}")
        self._publish_state()

    def update_state(self, event):
        self.logger.debug(f"Updating state with event: {event}")
        self._publish_state()

    def get_state(self):
        thermostat_state = ThermostatState(
            current_temperature=self._current_temperature, 
            target_temperature=self._target_temperature,
            current_humidity=self._current_humidity, 
            mode=self._mode, 
            fan_mode=self._fan_mode
        )
        return thermostat_state
