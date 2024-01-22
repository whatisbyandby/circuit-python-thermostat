from src.environment_sensor import sensor_task_setup, sensor_task_loop
from unittest.mock import patch
import pytest

def test_sensor_task_setup(mocker):

    class MockSensor:
        def start_readings(self):
            pass

    sensor = MockSensor()
    # spy on the start_readings method
    mocker.spy(sensor, 'start_readings')
    sensor_task_setup(sensor)
    # assert that the start_readings method was called
    sensor.start_readings.assert_called_once()

@pytest.mark.asyncio
async def test_sensor_task_loop(mocker):
    
        class MockThermostat:
            def handle_new_readings(self, readings):
                pass
    
        class MockSensor:
            def get_new_readings(self):
                return []

        # mock the call to asyncio.sleep
        mocker.patch('asyncio.sleep', return_value=None)
    
        thermostat = MockThermostat()
        sensor = MockSensor()
        # spy on the handle_new_readings method
        mocker.spy(thermostat, 'handle_new_readings')
        await sensor_task_loop(thermostat, sensor)
        # assert that the handle_new_readings method was called
        thermostat.handle_new_readings.assert_called_once()