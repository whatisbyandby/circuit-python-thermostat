import ThermostatSlider from "./ThermostatSlider";
import { useEffect, useReducer, useState } from 'react'
import { Button, Center, Loader } from "@mantine/core";
import { IconDropletFilled, IconTemperatureFahrenheit } from "@tabler/icons-react";
import ThermostatModeContainer from "./ThermostatModeButtons";
import useWebSocket from 'react-use-websocket';


export interface ThermostatProps {
    min: number;
    max: number;
}

export interface ThermostatState {
    currentTemperature: number;
    targetTemperature: number;
    currentHumidity: number;
    fanMode: string;
    thermostatAction: string;
    mode: string;
    isEditing: boolean;
}

export interface ThermostatUpdateState {
    currentTemperature: number;
    targetTemperature: number;
    currentHumidity: number;
    fanMode: string;
    thermostatAction: string;
    mode: string;
}

export function getModeColor(mode: string) {
    switch (mode) {
        case "auto":
            return "green"
        case "heat":
            return "orange"
        case "fan_only":
            return "blue"
        case "off":
            return "gray"
        default:
            return "gray"
    }
}

interface ThermostatAction {
    type: string;
    payload: any;

}

function stateReducer(state: ThermostatState, action: ThermostatAction): ThermostatState {
    switch (action.type) {
        case "update":
            if (state.isEditing) return { ...state };
            return { ...state, ...action.payload }
        case "setMode":
            return { ...state, mode: action.payload.mode, isEditing: true }
        case "finishedEditing":
            return { ...state, isEditing: false }
        case "updateTargetTemp":
            return { ...state, targetTemperature: action.payload.targetTemperature, isEditing: true }
        default:
            return { ...state }
    }
}

export default function Thermostat(props: ThermostatProps) {

    const { min, max } = props
    const socketUrl = "ws://localhost:8000/ws";

    const {
        sendJsonMessage
    } = useWebSocket(socketUrl, {
        onOpen: () => console.log('opened'),
        onMessage(event) {
            const data = JSON.parse(event.data);
            dispatch({
                type: "update", payload: {
                    currentTemperature: data.current_temperature,
                    targetTemperature: data.target_temperature,
                    currentHumidity: data.current_humidity,
                    fanMode: data.fan_mode,
                    thermostatAction: data.thermostat_action,
                    mode: data.mode
                }
            })
        },
        shouldReconnect: (closeEvent) => true,
    });

    const [thermostatState, dispatch] = useReducer(stateReducer, { currentTemperature: 0, targetTemperature: 0, currentHumidity: 0, fanMode: "", thermostatAction: "", mode: "", isEditing: false });

    if (!thermostatState) {
        return (
            <Center>
                <Loader color="blue" type="bars" />
            </Center>
        )
    }

    function setMode(mode: string) {
        dispatch({ type: "setMode", payload: { mode } })
        sendJsonMessage({ mode, target_temperature: thermostatState.targetTemperature })
        setTimeout(() => {
            dispatch({ type: "finishedEditing", payload: {} })
        }, 500);
    }

    function updateTargetTemperature(value: number) {
        dispatch({ type: "updateTargetTemperature", payload: { targetTemperature: value } })
        sendJsonMessage({ mode: thermostatState.mode, target_temperature: value });
        setTimeout(() => {
            dispatch({ type: "finishedEditing", payload: {} })
        }, 500);
    }


    return (
        <div>
            <h1>{thermostatState.thermostatAction}</h1>
            <ThermostatSlider
                targetTemperature={thermostatState.targetTemperature}
                updateTargetTemperature={updateTargetTemperature}
                min={min}
                max={max}
                mode={thermostatState.mode}
            />
            <h1>{Math.round(thermostatState.targetTemperature)} <IconTemperatureFahrenheit /></h1>
            <h2>{Math.round(thermostatState.currentTemperature)} <IconTemperatureFahrenheit size="16px" /></h2>
            <h2><IconDropletFilled />{Math.round(thermostatState.currentHumidity)} <span>%</span></h2>
            <ThermostatModeContainer mode={thermostatState.mode} setMode={setMode} />
        </div>
    )
}
