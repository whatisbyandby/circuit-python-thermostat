from src.thermostat import Thermostat, ThermostatMode
from src.environment_sensor import Reading
from src.switch import RelaySwitch

class TestQueue:

    queue = []

    def put_nowait(self, state):
        self.queue.append(state)

    def get(self):
        return self.queue.pop(0)
    

def test_thermostat_init(mocker):
    test_queue = TestQueue()

    mock_heater_switch = RelaySwitch(1)
    mock_fan_switch = RelaySwitch(1)

    t = Thermostat("test", heater_switch=mock_heater_switch, fan_switch=mock_fan_switch, state_queue=test_queue)
    assert t.device_id == "test"
    assert t._current_temperature == None
    assert t._current_humidity == None
    assert t._mode == ThermostatMode.HEAT
    assert t.logger.name == "Thermostat"

def test_thermostat_handle_new_readings():
    test_queue = TestQueue()
    mock_heater_switch = RelaySwitch(1)
    mock_fan_switch = RelaySwitch(1)
    t = Thermostat("test", heater_switch=mock_heater_switch, fan_switch=mock_fan_switch, state_queue=test_queue)

    t.handle_new_readings([
        Reading(measurement_type="temperature", value=72, unit="F"),
        Reading(measurement_type="humidity", value=40, unit="%")
    ])
    assert t._current_temperature == 72
    assert t._current_humidity == 40

    state = test_queue.get()
    assert state.current_temperature == 72
    assert state.current_humidity == 40
