NOT_IMPLEMENTED_MESSAGE = 'Subclass must implement this abstract method'


class Output():

    def set_water_heater_on(self, state=True):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)

    def set_air_heater_on(self, state=True):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)

    def set_grow_media_heater_on(self, state=True):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)

    def set_light_on(self, state=True):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)


class Input():

    def get_water_c(self):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)

    def get_air_c(self):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)

    def get_grow_media_c(self):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)

    def light_is_on(self):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)

    def water_heater_is_on(self):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)

    def air_heater_is_on(self):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)

    def grow_media_heater_is_on(self):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)
