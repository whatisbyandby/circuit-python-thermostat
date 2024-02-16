import logging
import json
import dataclasses

async def producer_loop(client, state_queue):    
    new_state = await state_queue.get()
    logger = logging.getLogger("State Publisher")
    await client.publish("home/thermostat/target_temp/state", new_state.target_temperature)
    await client.publish("home/thermostat/current_temp/state", new_state.current_temperature)
    await client.publish("home/thermostat/current_humidity/state", new_state.current_humidity)
    await client.publish("home/thermostat/mode/state", new_state.mode)
    await client.publish("home/thermostat/fan_mode/state", new_state.fan_mode)
    await client.publish("home/thermostat/action/state", new_state.thermostat_action)
    

async def producer_task(client, state_queue):
    logger = logging.getLogger("State Publisher Task")
    logger.info("Starting state publisher task")
    while True:
        await producer_loop(client, state_queue)