import React, { useEffect, useState } from 'react'
import Thermostat, { ThermostatState } from './Thermostat'

export default function WebsocketComponent() {
    const [websocket, setWebsocket] = useState<WebSocket | null>(null)
    const [thermostatState, setThermostatState] = useState<ThermostatState | null>(null)

    useEffect(() => {
        const ws = new WebSocket('ws://localhost:8000/ws')
        ws.onopen = () => {
            console.log('Connected')
        }
        ws.onmessage = (event) => {
            const parsedState = JSON.parse(event.data)
            setThermostatState({
                currentTemperature: parsedState.current_temperature,
                targetTemperature: parsedState.target_temperature,
                currentHumidity: parsedState.current_humidity,
                fanMode: parsedState.fan_mode,
                thermostatAction: parsedState.thermostat_action,
                mode: parsedState.mode
            })
        }
        ws.onclose = () => {
            console.log('Disconnected')
        }
        setWebsocket(ws)
    }, [])

    function sendState(newState: ThermostatState) {
        setThermostatState(newState)
        if (websocket) {
            websocket.send(JSON.stringify({
                target_temperature: newState.targetTemperature
            }))
        }
    }


    return (<>
        <Thermostat thermostatState={thermostatState} updateState={sendState} min={45} max={95} />
    </>)
}
