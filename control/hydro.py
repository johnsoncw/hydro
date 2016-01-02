from database.hydro import get_db_session, get_current_crop, get_current_crop_phase, get_control_set, set_next_phase
from input_output import get_input_interface, get_output_interface
from datetime import datetime


def _adjust(control_set):
    if control_set is not None:
        now = datetime.now()
        hours_now = now.hour + now.minute / 60.0
        ext_ip = get_input_interface()
        ext_op = get_output_interface()
        light_should_be_on = control_set.light_on_h <= hours_now <= control_set.light_off_h
        ext_op.set_light_on(light_should_be_on)
        water_heater_should_be_on = ext_ip.get_water_temp_c() < control_set.water_temp_C
        ext_op.set_water_heater_on(water_heater_should_be_on)
        air_heater_should_be_on = ext_ip.get_air_temp_c() < control_set.air_temp_C
        ext_op.set_air_heater_on(air_heater_should_be_on)


def _sound_alarm():
    pass


def _make_safe():
        ext_op = get_output_interface()
        ext_op.set_light_on(False)
        ext_op.set_water_heater_on(False)
        ext_op.set_air_heater_on(False)


def adjust_outputs():
    session = get_db_session()
    crop = get_current_crop(session)
    phase = get_current_crop_phase(session, crop)
    if phase is not None:
        now = datetime.now()
        hours_in_phase = (now - crop.current_phase_start).seconds / 3600.0
        if hours_in_phase > phase.duration_h:
            phase = set_next_phase(session, crop, phase)
        control_set = get_control_set(session, phase)
        _adjust(control_set)
    else:
        _make_safe()
        _sound_alarm()
