import logging
import asyncio
from enum import Enum
from dataclasses import dataclass
import os


@dataclass
class ThermostatState:
    current_temperature: float
    target_temperature: float
    current_humidity: float
    fan_mode: str
    thermostat_action: str
    mode: str


class ThermostatMode(str, Enum):
    OFF = "off"
    HEAT = "heat"
    COOL = "cool"
    AUTO = "auto"
    FAN_ONLY = "fan_only"


class ThermostatAction(str, Enum):
    HEATING = "heating"
    COOLING = "cooling"
    FAN = "fan"
    IDLE = "idle"
    OFF = "off"


class FanMode(str,
 Enum):
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

class ThermostatCommandType(str, Enum):
    SET_TARGET_TEMP = "target_temp"
    SET_MODE = "mode"
    SET_FAN_MODE = "fan_mode"
    SET_UNITS = "units"
    SET_STATE = "state"

@dataclass
class ThermostatCommand:
    command_type: ThermostatCommandType
    parameter: str


class Thermostat:
    def __init__(self, device_id, heater_switch=None, fan_switch=None, state_queue=None, cooler_switch=None):
        self.device_id = device_id
        self.logger = logging.getLogger("Thermostat")
        self._state_queue = state_queue
        self._current_temperature = int(os.getenv("DEFAULT_TEMP", 60))
        self._temperature_range = 1
        self._target_temperature = int(os.getenv("DEFAULT_TARGET_TEMP", 60))
        self._current_humidity = None
        self._mode = ThermostatMode.HEAT
        self._action: ThermostatAction = ThermostatAction.OFF
        self._fan_mode = FanMode.AUTO
        self._units = os.getenv("DEFAULT_UNITS", TemperatureUnits.F)
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
        self.logger.info(f"Handling command: {command}")
        if command.command_type == ThermostatCommandType.SET_TARGET_TEMP:
            self._target_temperature = float(command.parameter)
        elif command.command_type == ThermostatCommandType.SET_MODE:
            self._mode = command.parameter
        elif command.command_type == ThermostatCommandType.SET_FAN_MODE:
            self._fan_mode = command.parameter
        elif command.command_type == ThermostatCommandType.SET_UNITS:
            self._units = command.parameter
        elif command.command_type == ThermostatCommandType.SET_STATE:
            self._state = command.parameter
        else:
            self.logger.error(f"Unknown command: {command}")
        self._publish_state()


    def update_state(self, event_type):
        if event_type == ThermostatEventType.OVER_TEMPERATURE:
            self.heater_switch.off()
            self.fan_switch.off()
            self._action = ThermostatAction.IDLE
            
        elif event_type == ThermostatEventType.UNDER_TEMPERATURE:
            self.heater_switch.on()
            self.fan_switch.off()
            self._action = ThermostatAction.HEATING
           
        elif event_type == ThermostatEventType.TEMP_IN_RANGE:
            self.heater_switch.off()
            self.fan_switch.off()
            self._action = ThermostatAction.IDLE
        
        self.logger.debug(f"Updating state with event: {event_type}")
        self._publish_state()


    def get_state(self):
        thermostat_state = ThermostatState(
            current_temperature=self._current_temperature, 
            target_temperature=self._target_temperature,
            current_humidity=self._current_humidity, 
            thermostat_action=self._action,
            mode=self._mode, 
            fan_mode=self._fan_mode
        )
        return thermostat_state
