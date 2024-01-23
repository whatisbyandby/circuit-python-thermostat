from typing import Protocol
import digitalio

class Switch(Protocol):

    def turn_on(self) -> None:
        pass

    def turn_off(self) -> None:
        pass

    def is_on(self) -> bool:
        pass

class RelaySwitch(Switch):

    def __init__(self, pin: int):
        self.digitalPin = digitalio.DigitalInOut(board.D18)
        self.pinDirection = digitalio.Direction.OUTPUT

    def turn_on(self) -> None:
        self.digitalPin.value = True

    def turn_off(self) -> None:
        self.digitalPin.value = False

    def is_on(self) -> bool:
        return self.digitalPin.value