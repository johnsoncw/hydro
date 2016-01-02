from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, ForeignKey, Boolean, Numeric, Integer, String, DateTime, desc
from sqlalchemy.orm import sessionmaker, relationship
from os import path
from datetime import datetime

db_filename = 'hydro.db'
Base = declarative_base()


class ControlSet(Base):
    __tablename__ = 'control_set'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    air_temp_C = Column(Numeric(3, 2), nullable=False)
    water_temp_C = Column(Numeric(3, 2), nullable=False)
    light_on_h = Column(Numeric(3, 2), nullable=False)
    light_off_h = Column(Numeric(3, 2), nullable=False)


class CropPhase(Base):
    __tablename__ = 'crop_phase'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    control_set_id = Column(Integer)
    crop_id = Column(Integer, ForeignKey('crop.id'))
    sequence = Column(Integer, nullable=False)
    duration_h = Column(Numeric(3, 2), nullable=False)


class Crop(Base):
    __tablename__ = 'crop'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    phases = relationship(CropPhase)
    current_phase_id = Column(Integer)
    current_phase_start = Column(DateTime)
    sow_datetime = Column(DateTime)
    harvest_datetime = Column(DateTime)


class Measurement(Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    crop_id = Column(Integer)
    datetime = Column(DateTime, nullable=False)
    water_temp_C = Column(Numeric(3, 2), nullable=False)
    air_temp_C = Column(Numeric(3, 2), nullable=False)
    light_is_on = Column(Boolean, nullable=False)


def _create_default_entries(engine):
    session = sessionmaker(bind=engine)()
    sg = ControlSet(
            name='germinate',
            air_temp_C=25.0, water_temp_C=22.0,
            light_on_h=0.0, light_off_h=0.0)
    session.add(sg)
    ss = ControlSet(
            name='seedlings',
            air_temp_C=21.0, water_temp_C=19.0,
            light_on_h=8.0, light_off_h=23.0)
    session.add(ss)
    sm = ControlSet(
            name='main',
            air_temp_C=20.0, water_temp_C=16.0,
            light_on_h=8.0, light_off_h=23.0)
    session.add(sm)
    session.commit()
    c = Crop(name='lettuce')
    session.add(c)
    session.commit()
    p1 = CropPhase(
            name='1st', control_set_id=sg.id, crop_id=c.id,
            sequence=1, duration_h=(24.0 * 4.0))
    session.add(p1)
    p2 = CropPhase(
            name='2nd', control_set_id=ss.id, crop_id=c.id,
            sequence=2, duration_h=(24.0 * 6.0))
    session.add(p2)
    p3 = CropPhase(
            name='3rd', control_set_id=sm.id, crop_id=c.id,
            sequence=2, duration_h=(24.0 * 15.0))
    session.add(p3)
    session.commit()
    c.current_phase_id = p1.id
    c.current_phase_start = datetime.now()
    session.add(c)
    session.commit()


def get_db_session():
    engine = create_engine('sqlite:///' + db_filename)
    if path.isfile(db_filename):
        Base.metadata.bind = engine
    else:
        Base.metadata.create_all(engine)
        _create_default_entries(engine)
    factory = sessionmaker(bind=engine)
    return factory()


def get_current_crop(session):
    crop = session.query(Crop).filter(Crop.sow_datetime is not None).\
        order_by(desc(Crop.sow_datetime)).first()
    if crop is not None and crop.harvest_datetime is None:
        return crop
    return None


def get_current_crop_phase(session, crop):
    current_phase = None
    if crop is not None:
        current_phase = session.query(CropPhase).filter(CropPhase.crop_id == crop.current_phase_id).one()
    return current_phase


def get_control_set(session, phase):
    control_set = None
    if phase is not None:
        control_set = session.query(ControlSet).filter(phase.control_set_id)
    return control_set


def set_next_phase(session, crop, phase):
    next_phase = None
    if phase is not None:
        next_seq_num = phase.sequence + 1
        if crop is not None:
            next_phase = session.query(CropPhase).\
                filter(CropPhase.crop_id == crop.id).\
                filter(CropPhase.sequence == next_seq_num)
            if next_phase is None:
                next_phase = phase
            else:
                crop.current_phase_start = datetime.now()
                crop.current_phase_id = next_phase.id
                session.add(crop)
                session.commit()
    return next_phase


def store_measurement(air_temp_c, water_temp_c, light_is_on):
    session = get_db_session()
    crop = get_current_crop(session)
    if crop is not None and crop.harvest_datetime is None:
        m = Measurement(
                datetime=datetime.now(), crop_id=crop.id,
                air_temp_C=air_temp_c, water_temp_C=water_temp_c,
                light_is_on=light_is_on)
        session.add(m)
        session.commit()

