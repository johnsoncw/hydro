from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, ForeignKey, Boolean, Numeric, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from os import path
from datetime import datetime

db_filename = 'hydro.db'
Base = declarative_base()


class Strategy(Base):
    __tablename__ = 'strategy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    air_temp_C = Column(Numeric(3, 2), nullable=False)
    water_temp_C = Column(Numeric(3, 2), nullable=False)
    light_on_h = Column(Numeric(3, 2), nullable=False)
    light_off_h = Column(Numeric(3, 2), nullable=False)


class Crop(Base):
    __tablename__ = 'crop'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    strategy_id = Column(Integer, ForeignKey('strategy.id'))
    strategy = relationship(Strategy)
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)


class Measurement(Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    crop_id = Column(Integer, ForeignKey('crop.id'))
    crop = relationship(Crop)
    datetime = Column(DateTime, nullable=False)
    water_temp_C = Column(Numeric(3, 2), nullable=False)
    air_temp_C = Column(Numeric(3, 2), nullable=False)
    light_is_on = Column(Boolean, nullable=False)


def _create_default_entries(engine):
    session = sessionmaker(bind=engine)()
    s = Strategy(
            name='default',
            air_temp_C=20.0, water_temp_C=16.0,
            light_on_h=8.5, light_off_h=23.0)
    session.add(s)
    c = Crop(name='default', strategy=s)
    session.add(c)
    m = Measurement(
        crop=c, datetime=datetime.now(),
        water_temp_C=16.5, air_temp_C=19.5,
        light_is_on=False)
    session.add(m)
    session.commit()


def connect_to_db():
    engine = create_engine('sqlite:///' + db_filename)
    if path.isfile(db_filename):
        Base.metadata.bind = engine
    else:
        Base.metadata.create_all(engine)
        _create_default_entries(engine)
    factory = sessionmaker(bind=engine)
    return factory()
