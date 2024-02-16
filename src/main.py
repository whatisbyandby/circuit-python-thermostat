import board
import os
import logging
import dataclasses
import asyncio
import aiomqtt

from subscriber import subscriber_task
from producer import producer_task
from environment_sensor import get_environment_sensor, sensor_task
from thermostat import Thermostat
from utils import get_device_id
from switch import RelaySwitch
from dotenv import load_dotenv
from discovery import send_discovery_message
from thermostat import ThermostatCommand, ThermostatCommandType
from server import start_server


async def main():
    load_dotenv()
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.INFO)

    
    logger = logging.getLogger("Main")
    state_queue = asyncio.Queue()
    local_state_queue = asyncio.Queue()

    device_id = get_device_id()
    logger.info(f"Device ID: {device_id}")

    heater_switch = RelaySwitch(board.D12)
    fan_switch = RelaySwitch(board.D13)

    thermostat = Thermostat(
        device_id, 
        heater_switch=heater_switch, 
        fan_switch=fan_switch, 
        state_queue=state_queue,
        local_state_queue=local_state_queue
    )

    try:

        i2c = board.I2C()
        sensor = get_environment_sensor(i2c)

        start_server(thermostat, local_state_queue)

        async with aiomqtt.Client(os.getenv("MQTT_HOST")) as client:

            await send_discovery_message(client, thermostat)

            async with asyncio.TaskGroup() as tg:
                tg.create_task(sensor_task(thermostat, sensor))
                tg.create_task(subscriber_task(client, thermostat))
                tg.create_task(producer_task(client, state_queue))
    except Exception as e:
        logger.info(e)
        

if __name__ == "__main__":
    asyncio.run(main())