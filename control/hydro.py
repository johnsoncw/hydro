from database.hydro import Strategy, Crop, connect_to_db
from input_output import external
from datetime import datetime


def _adjust(crop, strategy):
    now = datetime.now()
    hours_now = now.hour() + now.minute() / 60.0
    ext_ip = external.get_input_interface()
    ext_op = external.get_output_interface()
    light_should_be_on = strategy.light_on_h() <= hours_now <= strategy.light_off_h()
    ext_op.set_light_on(light_should_be_on)
    water_heater_should_be_on = strategy.water_temp_C

def adjust_outputs():
    session = connect_to_db()
    c = session.query(Crop).order_by('start_datetime').last()
    if c.end_datetime() is None:
        s = session.query(Strategy).filter(Strategy.id == c.strategy_id).one()
        _adjust(c, s)
