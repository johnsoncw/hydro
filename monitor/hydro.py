from input_output import get_input_interface
from database.hydro import store_measurement


def take_measurements():
    ext_ip = get_input_interface()
    store_measurement(
        ext_ip.get_air_c(),
        ext_ip.get_water_c(),
        ext_ip.get_grow_media_c(),
        ext_ip.light_is_on())
