import logging
import json

async def subscriber_task(client, thermostat):
    logger = logging.getLogger("Command Subscriber Task")
    logger.info("Starting Command Subscriber")
    await client.subscribe("home/thermostat/command")
    async for message in client.messages:
        command = json.loads(message.payload.decode("utf-8"))
        thermostat.handle_command(command)