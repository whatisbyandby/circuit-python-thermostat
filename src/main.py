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
import tkinter as tk
from tkinter import ttk
from thermostat import ThermostatCommand, ThermostatCommandType
import time


async def ui_loop(thermostat):
    logger = logging.getLogger("UI")
    window = tk.Tk()
    window.tk.call("source", "src/azure.tcl")
    window.tk.call("set_theme", "dark")
    logger.info("Starting UI")
    entry = tk.Entry()

    current_value = tk.DoubleVar(value=thermostat._target_temperature)


    # Initialize buttons as None for later reference
    heat_button = None
    fan_button = None
    off_button = None
    auto_button = None

    def update_button_styles():
        # Update button styles based on the current mode
        modes = {
            "heat": heat_button,
            "fan_only": fan_button,
            "off": off_button,
            "auto": auto_button
        }
        current_mode = thermostat._mode  # Replace with actual method to get current mode
        for mode, button in modes.items():
            if button:
                if mode == current_mode:
                    button.style = 'Accent.TButton' # Highlighted style with green background
                else:
                    button.style = None  # Default style with white background


     # Define the command functions for the buttons
    def set_mode(mode):
        thermostat.handle_command(ThermostatCommand(command_type=ThermostatCommandType.SET_MODE, parameter=mode))
        update_button_styles()

    def my_callback(event):
        logger.info(f"Value changed to {event}")
        thermostat.handle_command(ThermostatCommand(command_type=ThermostatCommandType.SET_TARGET_TEMP, parameter=current_value.get()))

    

    tk.Label(window, text="Target Temp").pack(padx = 5, pady = 5)
    ttk.Scale(
        window, 
        style='Tick.TScale',
        from_=45,
        to=95, 
        length=300,
        orient='horizontal',
        variable=current_value, 
        command=my_callback
    ).pack(padx = 5, pady = 5)

    button_frame = tk.Frame(window)
    button_frame.pack(padx=0, pady=5)

    # Create buttons and add them to the frame
    auto_button = ttk.Button(button_frame, text="Auto", command=lambda: set_mode("auto"))
    heat_button = ttk.Button(button_frame, text="Heat", command=lambda: set_mode("heat"))
    fan_button = ttk.Button(button_frame, text="Fan", command=lambda: set_mode("fan"))
    off_button = ttk.Button(button_frame, text="Off", command=lambda: set_mode("off"))

    auto_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    heat_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    fan_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    off_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    update_button_styles()
    while True:
        current_value.set(thermostat._target_temperature)
        update_button_styles()
        window.update()
        await asyncio.sleep(0.01)


async def main():
    load_dotenv()
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.INFO)

    
    logger = logging.getLogger("Main")
    state_queue = asyncio.Queue()

    device_id = get_device_id()
    logger.info(f"Device ID: {device_id}")

    heater_switch = RelaySwitch(board.D12)
    fan_switch = RelaySwitch(board.D13)

    thermostat = Thermostat(
        device_id, 
        heater_switch=heater_switch, 
        fan_switch=fan_switch, 
        state_queue=state_queue
    )

    i2c = board.I2C()
    sensor = get_environment_sensor(i2c)


    async with aiomqtt.Client(os.getenv("MQTT_HOST")) as client:

        await send_discovery_message(client, thermostat)

        async with asyncio.TaskGroup() as tg:
            tg.create_task(sensor_task(thermostat, sensor))
            tg.create_task(subscriber_task(client, thermostat))
            tg.create_task(producer_task(client, state_queue))
            tg.create_task(ui_loop(thermostat))
        

if __name__ == "__main__":
    asyncio.run(main())