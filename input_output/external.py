from input_output import simulated, raspberry
import os

NOT_IMPLEMENTED_MESSAGE = 'Subclass must implement this abstract method'


class Output():

    def set_water_heater_on(self, state=True):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)

    def set_air_heater_on(self, state=True):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)

    def set_light_on(self, state=True):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)


class Input():

    def get_water_temp_c(self):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)

    def get_air_temp_c(self):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)

    def light_is_on(self):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)

    def water_heater_is_on(self):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)

    def air_heater_is_on(self):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)


def get_input_interface():
    if os.name == 'nt':
        return simulated.SimulatedInput()
    return None


def get_output_interface():
    if os.name == 'nt':
        return simulated.SimulatedOutput()
    return None
