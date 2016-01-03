from datetime import datetime
from input_output import interfaces


class _Sim():
    water_heater_is_on = False
    air_heater_is_on = False
    grow_media_heater_is_on = False
    light_is_on = False

    _last_dt = None
    _ambient_temp = 16.0
    _water_temp = 15.0
    _air_temp = 18.0
    _grow_media_temp = 16.0

    _water_delta_on = 0.01
    _water_delta_off = -0.01
    _air_delta_on = 0.2
    _air_delta_off = -0.4
    _grow_media_delta_on = 0.05
    _grow_media_delta_off = -0.1

    @classmethod
    def _calc_delta_changes(cls):
        dt_now = datetime.now()
        if cls._last_dt is None:
            cls._last_dt = dt_now
        else:
            elapsed_s = (dt_now - cls._last_dt).total_seconds()
            if elapsed_s > 1.0:
                if cls.water_heater_is_on:
                    cls._water_temp += elapsed_s * cls._water_delta_on
                else:
                    if cls._water_temp > cls._ambient_temp:
                        cls._water_temp += elapsed_s * cls._water_delta_off
                    if cls._water_temp < cls._ambient_temp:
                        cls._water_temp -= elapsed_s * cls._water_delta_off
                if cls.air_heater_is_on:
                    cls._air_temp += elapsed_s * cls._air_delta_on
                else:
                    if cls._air_temp > cls._ambient_temp:
                        cls._air_temp += elapsed_s * cls._air_delta_off
                    if cls._air_temp < cls._ambient_temp:
                        cls._air_temp -= elapsed_s * cls._air_delta_off
                if cls.grow_media_heater_is_on:
                    cls._grow_media_temp += elapsed_s * cls._grow_media_delta_on
                else:
                    if cls._grow_media_temp > cls._ambient_temp:
                        cls._grow_media_temp += elapsed_s * cls._grow_media_delta_off
                    if cls._grow_media_temp < cls._ambient_temp:
                        cls._grow_media_temp -= elapsed_s * cls._grow_media_delta_off
                cls._last_dt = dt_now

    @classmethod
    def get_water_c(cls):
        cls._calc_delta_changes()
        return cls._water_temp

    @classmethod
    def get_air_c(cls):
        cls._calc_delta_changes()
        return cls._air_temp

    @classmethod
    def get_grow_media_c(cls):
        cls._calc_delta_changes()
        return cls._grow_media_temp


class SimulatedOutput(interfaces.Output):

    def set_grow_media_heater_on(self, state=True):
        _Sim.grow_media_heater_is_on = state

    def set_water_heater_on(self, state=True):
        _Sim.water_heater_is_on = state

    def set_air_heater_on(self, state=True):
        _Sim.air_heater_is_on = state

    def set_light_on(self, state=True):
        _Sim.light_is_on = state


class SimulatedInput(interfaces.Input):

    def get_grow_media_c(self):
        return _Sim.get_grow_media_c()

    def get_water_c(self):
        return _Sim.get_water_c()

    def get_air_c(self):
        return _Sim.get_air_c()

    def light_is_on(self):
        return _Sim.light_is_on

    def water_heater_is_on(self):
        return _Sim.water_heater_is_on

    def air_heater_is_on(self):
        return _Sim.air_heater_is_on

    def grow_media_heater_is_on(self):
        pass
