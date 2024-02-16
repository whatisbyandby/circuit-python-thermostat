import { Button, Center } from "@mantine/core";
import { IconFlame, IconPower, IconPropeller, IconRefresh } from "@tabler/icons-react";


interface ThermostatModeButtonProps {
    icon: JSX.Element;
    isActive: boolean;
    mode: string;
    setMode: (mode: string) => void;
    activeColor: string;
}

function ModeButton(props: ThermostatModeButtonProps) {

    const { mode, setMode, isActive, activeColor, icon } = props;

    return <Button
        size="xl"
        color={isActive ? activeColor : "gray"}
        onClick={() => setMode(mode)}
    >
        {icon}
    </Button>
}

interface ThermostatModeContainerProps {
    mode: string;
    setMode: (mode: string) => void;
}

export default function ThermostatModeContainer(props: ThermostatModeContainerProps) {

    const { mode, setMode } = props;

    return (<Center>
        <Button.Group>
            <ModeButton mode="auto" setMode={setMode} isActive={mode === "auto"} activeColor="green" icon={<IconRefresh />} />
            <ModeButton mode="heat" setMode={setMode} isActive={mode === "heat"} activeColor="orange" icon={<IconFlame />} />
            <ModeButton mode="fan_only" setMode={setMode} isActive={mode === "fan_only"} activeColor="blue" icon={<IconPropeller />} />
            <ModeButton mode="off" setMode={setMode} isActive={mode === "off"} activeColor="gray" icon={<IconPower />} />
        </Button.Group>
    </Center>)
}