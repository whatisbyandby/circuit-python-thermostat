import logging
import json
import dataclasses

async def producer_loop(client, state_queue):    
    new_state = await state_queue.get()
    await client.publish("home/thermostat/state", json.dumps(dataclasses.asdict(new_state)))

async def producer_task(client, state_queue):
    logger = logging.getLogger("State Publisher Task")
    logger.info("Starting state publisher task")
    while True:
        await producer_loop(client, state_queue)