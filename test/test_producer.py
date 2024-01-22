from src.producer import producer_loop
from src.thermostat import ThermostatState
import dataclasses
import pytest

@pytest.mark.asyncio
async def test_producer_loop(mocker):

    class MockClient:
        async def publish(self, topic, payload):
            pass

    class MockStateQueue:
        
        async def get(self):
            thermostat_state = ThermostatState(
                current_temperature=10,
                current_humidity=20,
                target_temperature=25,
                fan_mode="auto",
                mode="off",
            )
            return thermostat_state


    client = MockClient()
    state = MockStateQueue()
    mocker.patch('dataclasses.asdict', return_value={'temperature': 10, 'humidity': 20})
    mocker.spy(client, 'publish')
    mocker.spy(state, 'get')
    await producer_loop(client, state)
    state.get.assert_called_once()
    client.publish.assert_called_once()
    client.publish.assert_called_with("home/thermostat/state", '{"temperature": 10, "humidity": 20}')