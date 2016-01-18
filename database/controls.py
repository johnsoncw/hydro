from sqlalchemy import Column, Numeric, Integer, String
from sqlalchemy.orm.exc import NoResultFound

from database import Base


class ControlSet(Base):
    __tablename__ = 'control_set'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    air_C = Column(Numeric(3, 2), nullable=False)
    water_C = Column(Numeric(3, 2), nullable=False)
    grow_media_C = Column(Numeric(3, 2), nullable=False)
    light_on_h = Column(Numeric(3, 2), nullable=False)
    light_off_h = Column(Numeric(3, 2), nullable=False)


def get_control_set(session, phase):
    control_set = None
    if phase is not None:
        control_set = session.query(ControlSet). \
            filter(ControlSet.id == phase.control_set_id). \
            one()
    return control_set


def get_control_set_by_name(session, name):
    try:
        return session.query(ControlSet).filter(ControlSet.name == name).one()
    except NoResultFound:
        print("No control set named " + name)
    return None


def init_control_sets(session):
    sg = ControlSet(
            name='default germinate',
            air_C=25.0, water_C=22.0, grow_media_C=22.0,
            light_on_h=0.0, light_off_h=0.0)
    session.add(sg)
    ss = ControlSet(
            name='default seedlings',
            air_C=21.0, water_C=19.0, grow_media_C=19.0,
            light_on_h=8.0, light_off_h=23.0)
    session.add(ss)
    sm = ControlSet(
            name='default main',
            air_C=20.0, water_C=16.0, grow_media_C=16.0,
            light_on_h=8.0, light_off_h=23.0)
    session.add(sm)
    session.commit()


