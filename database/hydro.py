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
    air_C = Column(Numeric(3, 2), nullable=False)
    water_C = Column(Numeric(3, 2), nullable=False)
    grow_media_C = Column(Numeric(3, 2), nullable=False)
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
    water_C = Column(Numeric(3, 2), nullable=False)
    air_C = Column(Numeric(3, 2), nullable=False)
    grow_media_C = Column(Numeric(3, 2), nullable=False)
    light_is_on = Column(Boolean, nullable=False)


def _initialise_control_sets(session):
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


def get_db_session():
    engine = create_engine('sqlite:///' + db_filename)
    if path.isfile(db_filename):
        Base.metadata.bind = engine
        factory = sessionmaker(bind=engine)
        return factory()
    else:
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)()
        _initialise_control_sets(session)
        return session


def get_current_crop(session):
    crop = session.query(Crop).\
        filter(Crop.sow_datetime is not None).\
        order_by(desc(Crop.sow_datetime)).\
        first()
    if crop is None or crop.harvest_datetime is not None:
        # no crop or last crop is done
        return None
    return crop


def get_current_crop_phase(session, crop):
    current_phase = None
    if crop is not None:
        current_phase = session.query(CropPhase).\
            filter(CropPhase.crop_id == crop.id).\
            filter(CropPhase.id == crop.current_phase_id).\
            one()
    return current_phase


def get_control_set(session, phase):
    control_set = None
    if phase is not None:
        control_set = session.query(ControlSet).\
            filter(ControlSet.id == phase.control_set_id).\
            one()
    return control_set


def set_next_phase(session, crop, phase):
    next_phase = None
    if phase is not None:
        next_seq_num = phase.sequence + 1
        if crop is not None:
            next_phase = session.query(CropPhase).\
                filter(CropPhase.crop_id == crop.id).\
                filter(CropPhase.sequence == next_seq_num).\
                one()
            if next_phase is None:
                next_phase = phase
            else:
                crop.current_phase_start = datetime.now()
                crop.current_phase_id = next_phase.id
                session.add(crop)
                session.commit()
    return next_phase


def store_measurement(air_c, water_c, grow_media_c, light_is_on):
    session = get_db_session()
    crop = get_current_crop(session)
    if crop is not None and crop.harvest_datetime is None:
        m = Measurement(
                datetime=datetime.now(), crop_id=crop.id,
                air_C=air_c, water_C=water_c, grow_media_C=grow_media_c,
                light_is_on=light_is_on)
        session.add(m)
        session.commit()

