import { Slider } from '@mantine/core';
import { useEffect, useState } from 'react';
import { getModeColor } from './Thermostat';


export interface ThermostatSliderProps {
    targetTemperature: number;
    updateTargetTemperature: (value: number) => void;
    min: number;
    max: number;
    mode: string;
}


function generateMarks(low: number, high: number) {
    const marks = [];
    const step = (high - low) / 10;
    for (let i = 0; i <= 10; i++) {
        const value = low + step * i;
        marks.push({ value: Math.round(value), label: `${Math.round(value)}°` });
    }
    return marks;
}


export default function ThermostatSlider(props: ThermostatSliderProps) {
    const {
        targetTemperature,
        updateTargetTemperature,
        min,
        max
    } = props;
    console.log(targetTemperature)

    const [targetTemperatureValue, setTargetTemperature] = useState(targetTemperature);

    useEffect(() => {
        setTargetTemperature(targetTemperature);
    }, [targetTemperature]);

    const marks = generateMarks(min, max);

    return (
        <Slider
            min={min}
            max={max}
            marks={marks}
            disabled={props.mode === "off"}
            color={getModeColor(props.mode)}
            value={targetTemperatureValue}
            onChange={setTargetTemperature}
            onChangeEnd={updateTargetTemperature}
        />
    );
}