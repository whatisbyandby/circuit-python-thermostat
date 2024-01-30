import threading
import uvicorn
from fastapi import FastAPI, WebSocket
import json
from thermostat import ThermostatCommand, ThermostatCommandType
import dataclasses
import asyncio


def start_server(thermostat, queue):

    app = FastAPI()

    async def process_websocket(websocket: WebSocket, queue: asyncio.Queue):
        while True:
            try:
                data = await websocket.receive_text()
                json_data = json.loads(data)
                await queue.put(json_data)
            except WebSocketDisconnect:
                break

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        command_queue = asyncio.Queue()
        task = asyncio.create_task(process_websocket(websocket, command_queue))
        while True:
            if not queue.empty():
                current_state = await queue.get()
                await websocket.send_text(json.dumps(dataclasses.asdict(current_state)))
            if not command_queue.empty():
                message = await command_queue.get()
                thermostat.handle_command(ThermostatCommand(command_type=ThermostatCommandType.SET_TARGET_TEMP, parameter=message.get("target_temperature")))
            await asyncio.sleep(0.2)
    
    def run_fastapi():
        uvicorn.run(app, host="0.0.0.0", port=8000)

    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()