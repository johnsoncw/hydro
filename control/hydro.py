from datetime import datetime
import database.core
import database.crops
import database.controls
import input_output


def _adjust(control_set, simulated):
    if control_set is not None:
        now = datetime.now()
        hours_now = now.hour + now.minute / 60.0
        ext_ip = input_output.get_input_interface(simulated)
        ext_op = input_output.get_output_interface(simulated)
        light_should_be_on = control_set.light_on_h <= hours_now <= control_set.light_off_h
        ext_op.set_light_on(light_should_be_on)
        water_heater_should_be_on = ext_ip.get_water_c() < control_set.water_C
        ext_op.set_water_heater_on(water_heater_should_be_on)
        air_heater_should_be_on = ext_ip.get_air_c() < control_set.air_C
        ext_op.set_air_heater_on(air_heater_should_be_on)
        grow_media_heater_should_be_on = ext_ip.get_grow_media_c() < control_set.grow_media_C
        ext_op.set_grow_media_heater_on(grow_media_heater_should_be_on)


def _sound_alarm(message):
    # TODO: something more than printing a message
    print("Control Panic: " + message)


def _make_safe(simulated):
    ext_op = input_output.get_output_interface(simulated)
    ext_op.set_light_on(False)
    ext_op.set_water_heater_on(False)
    ext_op.set_air_heater_on(False)
    ext_op.set_grow_media_heater_on(False)


def adjust_outputs(crop_id):
    session = database.core.get_db_session()
    crop = database.crops.get_crop_by_id(session, crop_id)
    if crop is not None:
        phase = database.crops.get_current_crop_phase(session, crop)
        if phase is not None:
            now = datetime.now()
            hours_in_phase = (now - crop.current_phase_start).total_seconds() / 3600.0
            if hours_in_phase > phase.duration_h:
                phase = database.crops.set_next_phase(session, crop, phase)
            control_set = database.controls.get_control_set(session, phase)
            if control_set is not None:
                _adjust(control_set, crop.simulated)
            else:
                _make_safe(crop.simulated)
                _sound_alarm("No ControlSet")
        else:
            _make_safe(crop.simulated)
            _sound_alarm("No CropPhase")

