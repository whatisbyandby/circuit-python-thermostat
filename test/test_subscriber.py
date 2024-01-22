import pytest
from src.subscriber import subscriber_task

@pytest.mark.asyncio
async def test_subscriber_task(mocker):
    pass

    # class MockClient:
    #     async def subscribe(self, topic):
    #         pass

    #     @property
    #     def messages(self):
    #         pass

    # class MockThermostat:
    #     def handle_command(self, command):
    #         pass

    # client = MockClient()
    # thermostat = MockThermostat()
    # mocker.spy(client, 'subscribe')
    # mocker.spy(client, 'messages')
    # mocker.spy(thermostat, 'handle_command')
    # await subscriber_task(client, thermostat)
    # client.subscribe.assert_called_once()
    # client.messages.assert_called_once()
    # thermostat.handle_command.assert_called_once()


