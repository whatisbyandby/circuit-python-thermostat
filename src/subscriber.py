import logging
import json
from thermostat import ThermostatCommand

async def subscriber_task(client, thermostat):
    logger = logging.getLogger("Command Subscriber Task")
    logger.info("Starting Command Subscriber")
    await client.subscribe("home/thermostat/+/set")
    async for message in client.messages:
        topic = message.topic.value
        field = topic.split("/")[-2]
        value = message.payload.decode()
        thermostat.handle_command(ThermostatCommand(command_type=field, parameter=value))