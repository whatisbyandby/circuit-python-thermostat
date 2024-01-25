from typing import Protocol
import board
import digitalio

class Switch(Protocol):

    def on(self) -> None:
        pass

    def off(self) -> None:
        pass

    def is_on(self) -> bool:
        pass

class RelaySwitch(Switch):

    def __init__(self, pin):
        self.digitalPin = digitalio.DigitalInOut(pin)
        self.digitalPin.direction = digitalio.Direction.OUTPUT

    def on(self) -> None:
        self.digitalPin.value = True

    def off(self) -> None:
        self.digitalPin.value = False

    def is_on(self) -> bool:
        return self.digitalPin.value