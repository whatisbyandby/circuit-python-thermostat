import ThermostatSlider from "./ThermostatSlider";
import { Center, Loader } from "@mantine/core";


export interface ThermostatProps {
    thermostatState: ThermostatState | null;
    updateState: (state: ThermostatState) => void;
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
}

export default function Thermostat(props: ThermostatProps) {
    const {
        thermostatState,
        updateState,
        min,
        max
    } = props;

    if (!thermostatState) {
        return (
            <Center>
                <Loader color="blue" type="bars" />
            </Center>
        )
    }

    return (
        <div>
            <ThermostatSlider targetTemperature={thermostatState.targetTemperature}
                updateTargetTemperature={(value: number) => {
                    updateState({
                        ...thermostatState,
                        targetTemperature: value
                    })
                }
                } min={min} max={max} />
            <h1>{Math.round(thermostatState.targetTemperature)} <span>°F</span></h1>
            <h2>{Math.round(thermostatState.currentTemperature)} <span>°F</span></h2>
            <h2>{Math.round(thermostatState.currentHumidity)} <span>%</span></h2>
        </div>
    )
}
