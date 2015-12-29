from database.hydro import Measurement, Crop, connect_to_db
from input_output import external
from datetime import datetime


def take_measurements():
    ext_ip = external.get_input_interface()
    session = connect_to_db()
    c = session.query(Crop).first()
    m = Measurement(
        datetime=datetime.now(), crop=c,
        air_temp_C=ext_ip.get_air_temp_c(),
        water_temp_C=ext_ip.get_water_temp_c(),
        light_is_on=ext_ip.light_is_on())
    session.add(m)
    session.commit()
