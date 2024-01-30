import { Slider } from '@mantine/core';
import { useEffect, useState } from 'react';


export interface ThermostatSliderProps {
    targetTemperature: number;
    updateTargetTemperature: (value: number) => void;
    min: number;
    max: number;
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

    const [targetTemperatureValue, setTargetTemperature] = useState(targetTemperature);
    const marks = generateMarks(min, max);

    useEffect(() => {
        setTargetTemperature(targetTemperature);
    }, [targetTemperature]);

    return (
        <Slider
            min={min}
            max={max}
            marks={marks}
            value={targetTemperatureValue}
            onChange={setTargetTemperature}
            onChangeEnd={updateTargetTemperature}
        />
    );
}