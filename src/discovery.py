import logging
import json

async def send_discovery_message(client, thermostat):
    logger = logging.getLogger("Discovery")
    logger.info("Sending discovery message")
    discovery_message = {
        "name": "Thermostat",

        "action_topic": f"home/thermostat/{thermostat.device_id}/action/state",

        # Current Temperature
        "current_temperature_topic": f"home/thermostat/current_temp/state",

        # Current Humidity
        "current_humidity_topic": f"home/thermostat/current_humidity/state",

        # Target Temperature
        "temperature_state_topic": f"home/thermostat/target_temp/state",
        "temperature_command_topic": f"home/thermostat/target_temp/set",

        # Modes
        "modes": ["off", "heat", "auto", "fan_only"],
        "mode_state_topic": f"home/thermostat/mode/state",
        "mode_command_topic": f"home/thermostat/mode/set",

        # Fan Modes
        "fan_modes": ["auto", "low", "medium", "high"],
        "fan_mode_state_topic": f"home/thermostat/fan_mode/state",
        "fan_mode_command_topic": f"home/thermostat/fan_mode/set",

        # Optomistic
        "optimistic": "false",
        "retain": "true",
        
    }
    await client.publish(f"homeassistant/climate/{thermostat.device_id}/config", json.dumps(discovery_message), retain=True, qos=1)
    logger.info("Discovery message sent")