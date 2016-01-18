from sqlalchemy import Column, Boolean, Numeric, Integer, DateTime
from datetime import datetime

from database import Base


class Measurement(Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    crop_id = Column(Integer)
    phase_id = Column(Integer)
    datetime = Column(DateTime, nullable=False)
    water_C = Column(Numeric(3, 2), nullable=False)
    air_C = Column(Numeric(3, 2), nullable=False)
    grow_media_C = Column(Numeric(3, 2), nullable=False)
    light_is_on = Column(Boolean, nullable=False)


def store_measurement(session, crop, ext_if):
    if crop is not None and crop.harvest_datetime is None:
        m = Measurement(
                datetime=datetime.now(), crop_id=crop.id, phase_id=crop.current_phase_id,
                air_C=ext_if.get_air_c(), water_C=ext_if.get_water_c(),
                grow_media_C=ext_if.get_grow_media_c(), light_is_on=ext_if.light_is_on())
        session.add(m)
        session.commit()

