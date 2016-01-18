from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import path

from database import Base, db_filename
import database.controls
import database.crops


def get_db_session():
    engine = create_engine('sqlite:///' + db_filename)
    if path.isfile(db_filename):
        Base.metadata.bind = engine
        factory = sessionmaker(bind=engine)
        return factory()
    else:
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)()
        database.controls.init_control_sets(session)
        database.crops.init_crops(session)
        return session
