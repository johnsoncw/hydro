from input_output import get_input_interface
from database.hydro import store_measurement


def take_measurements():
    ext_ip = get_input_interface()
    store_measurement(
        ext_ip.get_air_temp_c(),
        ext_ip.get_water_temp_c(),
        ext_ip.light_is_on())
