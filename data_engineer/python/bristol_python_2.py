from abc import ABC, abstractmethod
from typing import Union


class LampSwitcher(ABC):

    def __init__(self) -> None:
        self.on_state = False

    @abstractmethod
    def turn_on(self) -> None:
        pass

    @abstractmethod
    def turn_off(self) -> None:
        pass


class GlowLampSwitcher(LampSwitcher):

    def turn_on(self) -> None:
        print('Лампа накаливания включена...')
        self.on_state = True

    def turn_off(self) -> None:
        print('Лампа накаливания выключена...')
        self.on_state = False


class HalogenLampSwitcher(LampSwitcher):

    def turn_on(self) -> None:
        print('Галогенная лампа включена...')
        self.on_state = True

    def turn_off(self) -> None:
        print('Галогенная лампа выключена...')
        self.on_state = False


class AnotherLampSwitcher(LampSwitcher):

    def turn_on(self) -> None:
        print('Ещё лампа включена...')
        self.on_state = True

    def turn_off(self) -> None:
        print('Ещё лампа выключена...')
        self.on_state = False


class ElectricLightSwitchManager:

    def __init__(self, switcher: LampSwitcher) -> None:
        self.switcher = switcher

    def press(self) -> None:
        if self.switcher.on_state:
            self.switcher.turn_off()
        else:
            self.switcher.turn_on()


def main() -> None:
    switch = ElectricLightSwitchManager(GlowLampSwitcher())
    switch.press()
    switch.press()
    switch = ElectricLightSwitchManager(HalogenLampSwitcher())
    switch.press()
    switch.press()
    switch = ElectricLightSwitchManager(AnotherLampSwitcher())
    switch.press()
    switch.press()


if __name__ == '__main__':
    main()
