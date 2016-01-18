from sqlalchemy import Column, ForeignKey, Boolean, Numeric, Integer, String, DateTime, desc
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

from database import Base
import database.core
import database.controls


class CropPhase(Base):
    __tablename__ = 'crop_phase'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    control_set_id = Column(Integer, nullable=False)
    crop_id = Column(Integer, ForeignKey('crop.id'))
    sequence = Column(Integer)
    duration_h = Column(Numeric(3, 2))


class Crop(Base):
    __tablename__ = 'crop'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    simulated = Column(Boolean)
    phases = relationship(CropPhase)
    current_phase_id = Column(Integer)
    current_phase_start = Column(DateTime)
    sow_datetime = Column(DateTime)
    harvest_datetime = Column(DateTime)


def _get_or_create_crop(session, crop_name):
    try:
        return session.query(Crop).filter(Crop.name == crop_name).one()
    except NoResultFound:
        return Crop(name=crop_name)


def _get_or_create_crop_phase(session, phase_name, control_set_id, crop_id, sequence):
    try:
        phase = session.query(CropPhase).filter(CropPhase.name == phase_name).one()
        phase.control_set_id = control_set_id
        phase.crop_id = crop_id
        phase.sequence = sequence
        return phase
    except NoResultFound:
        return CropPhase(name=phase_name, control_set_id=control_set_id, crop_id=crop_id, sequence=sequence)


def set_next_phase(session, crop, phase):
    next_phase = None
    if phase is not None:
        next_seq_num = phase.sequence + 1
        if crop is not None:
            next_phase = session.query(CropPhase). \
                filter(CropPhase.crop_id == crop.id). \
                filter(CropPhase.sequence == next_seq_num). \
                one()
            if next_phase is None:
                next_phase = phase
            else:
                crop.current_phase_start = datetime.now()
                crop.current_phase_id = next_phase.id
                session.add(crop)
                session.commit()
    return next_phase


def get_latest_crop(session):
    crop = session.query(Crop). \
        filter(Crop.sow_datetime is not None). \
        order_by(desc(Crop.sow_datetime)). \
        first()
    if crop is None or crop.harvest_datetime is not None:
        # no crop or last crop is done
        return None
    return crop


def get_current_crop_phase(session, crop):
    current_phase = None
    if crop is not None:
        current_phase = session.query(CropPhase). \
            filter(CropPhase.crop_id == crop.id). \
            filter(CropPhase.id == crop.current_phase_id). \
            one()
    return current_phase


def new_default_crop(session, name, simulated=False):
    germinate = database.controls.get_control_set_by_name(session, 'default germinate')
    seedlings = database.controls.get_control_set_by_name(session, 'default seedlings')
    main = database.controls.get_control_set_by_name(session, 'default main')
    if germinate is None or seedlings is None or main is None:
        return None
    else:
        now = datetime.now()
        day_h = 12.0  # hours
        crop = _get_or_create_crop(session, name)
        crop.simulated = simulated
        session.add(crop)
        session.commit()
        p1 = _get_or_create_crop_phase(
                session, '{0} germination'.format(name),
                control_set_id=germinate.id, crop_id=crop.id, sequence=1)
        p1.duration_h = (day_h * 4.0)
        session.add(p1)
        p2 = _get_or_create_crop_phase(
                session, '{0} seedlings'.format(name),
                control_set_id=seedlings.id, crop_id=crop.id, sequence=2)
        p2.duration_h = (day_h * 6.0)
        session.add(p2)
        p3 = _get_or_create_crop_phase(
                session, '{0} main'.format(name),
                control_set_id=main.id, crop_id=crop.id, sequence=3)
        p3.duration_h = (day_h * 15.0)
        session.add(p3)
        session.commit()
        crop.current_phase_id = p1.id
        crop.current_phase_start = now
        crop.sow_datetime = now
        session.add(crop)
        session.commit()
        return crop


def get_crop_by_id(session, crop_id):
    try:
        return session.query(Crop).filter(Crop.id == crop_id).one()
    except NoResultFound:
        return None


def get_crop_id(name, simulated=False, create=False):
    session = database.core.get_db_session()
    try:
        crop = session.query(Crop).filter(Crop.name == name and Crop.simulated == simulated).one()
        print("A {0} crop named {1} was found".format(("simulated" if simulated else ""),  name))
        return crop.id
    except NoResultFound:
        pass
    print("No {0} crop named {1}".format(("simulated" if simulated else ""),  name))
    if create:
        print("creating a default crop")
        crop = new_default_crop(session, name, simulated)
        return crop.id
    return None


def init_crops(session):
    pass
