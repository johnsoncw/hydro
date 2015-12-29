from database.hydro import Measurement, Crop, connect_to_db
from datetime import datetime


def take_measurements():
    session = connect_to_db()
    c = session.query(Crop).first()
    m = Measurement(
        datetime=datetime.now(), crop=c,
        air_temp_C=20.1, water_temp_C=16.0,
        light_is_on=True)
    session.add(m)
    session.commit()
