import board
from environment_sensor import get_environment_sensor, sensor_task
from producer import producer_task
from subscriber import subscriber_task
import logging
import dataclasses
import asyncio
import aiomqtt
from thermostat import Thermostat
from utils import get_device_id


async def main():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)
    
    logger = logging.getLogger("Main")
    state_queue = asyncio.Queue()

    device_id = get_device_id()
    logger.info(f"Device ID: {device_id}")

    thermostat = Thermostat(device_id, state_queue)
    i2c = board.I2C()
    sensor = get_environment_sensor(i2c)
    
    async with aiomqtt.Client("192.168.1.88") as client:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(sensor_task(thermostat, sensor))
            tg.create_task(subscriber_task(client, thermostat))
            tg.create_task(producer_task(client, state_queue))
        

if __name__ == "__main__":
    asyncio.run(main())