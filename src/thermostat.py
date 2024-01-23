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


class ThermostatState(str, Enum):
    HEAT_ON = "heat_on"
    COOL_ON = "cool_on"
    FAN_ON = "fan_on"
    OFF = "off"


class FanMode(str, Enum):
    AUTO = "auto"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TemperatureUnits(str, Enum):
    F = "F"
    C = "C"


class ThermostatEventType(str, Enum):
    OVER_TEMPERATURE = "over_temperature"
    UNDER_TEMPERATURE = "under_temperature"
    TEMP_IN_RANGE = "temp_in_range"


class Thermostat:
    def __init__(self, device_id, heater_switch=None, fan_switch=None, state_queue=None, cooler_switch=None):
        self.device_id = device_id
        self.logger = logging.getLogger("Thermostat")
        self._state_queue = state_queue
        self._current_temperature = None
        self._temperature_range = 1
        self._target_temperature = None
        self._current_humidity = None
        self._mode = ThermostatMode.HEAT
        self._state = ThermostatState.OFF
        self._fan_mode = FanMode.AUTO
        self._units = TemperatureUnits.F
        self._room = "living room"
        self.heater_switch = heater_switch
        self.fan_switch = fan_switch
        self.cooler_switch = cooler_switch


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
        self.check_temperature()
        self._publish_state()


    def check_temperature(self):
        if self._current_temperature > self._target_temperature + self._temperature_range:
            self.update_state(ThermostatEventType.OVER_TEMPERATURE)
        elif self._current_temperature < self._target_temperature - self._temperature_range:
            self.update_state(ThermostatEventType.UNDER_TEMPERATURE)
        else:
            self.update_state(ThermostatEventType.TEMP_IN_RANGE)


    def handle_command(self, command):
        self.logger.debug(f"Got command: {command}")
        self._publish_state()


    def update_state(self, event):
        if event.event_type == ThermostatEventType.OVER_TEMPERATURE:
            self.heater_switch.off()
            self.fan_switch.off()
            self._state = ThermostatState.OFF
            
        elif event.event_type == ThermostatEventType.UNDER_TEMPERATURE:
            self.heater_switch.on()
            self.fan_switch.off()
            self._state = ThermostatState.HEAT_ON
           
        elif event.event_type == ThermostatEventType.TEMP_IN_RANGE:
            self.heater_switch.off()
            self.fan_switch.off()
            self._mode = ThermostatState.OFF
        
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
