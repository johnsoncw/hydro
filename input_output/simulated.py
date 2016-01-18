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

    @staticmethod
    def _iterate(val, heater_on, elapsed_s, delta_on, delta_off):
        ambient_pull = elapsed_s * delta_off
        if val > _Sim._ambient_temp:
            ambient_pull *= -1
        if heater_on:
            return val + ambient_pull + elapsed_s * delta_on
        else:
            return val + ambient_pull

    @staticmethod
    def _calc_delta_changes():
        now = datetime.now()
        if _Sim._last_dt is None:
            _Sim._last_dt = now
        else:
            elapsed_s = (now - _Sim._last_dt).total_seconds()
            if elapsed_s > 1.0:
                _Sim._last_dt = now
                _Sim._water_temp = _Sim._iterate(
                        _Sim._water_temp, _Sim.water_heater_is_on, elapsed_s, 0.02, 0.01)
                _Sim._air_temp = _Sim._iterate(
                        _Sim._air_temp, _Sim.air_heater_is_on, elapsed_s, 0.4, 0.2)
                _Sim._grow_media_temp = _Sim._iterate(
                        _Sim._grow_media_temp, _Sim.grow_media_heater_is_on, elapsed_s, 0.02, 0.01)

    @staticmethod
    def get_water_c():
        _Sim._calc_delta_changes()
        return _Sim._water_temp

    @staticmethod
    def get_air_c():
        _Sim._calc_delta_changes()
        return _Sim._air_temp

    @staticmethod
    def get_grow_media_c():
        _Sim._calc_delta_changes()
        return _Sim._grow_media_temp


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
