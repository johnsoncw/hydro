from database.hydro import Crop, CropPhase, ControlSet
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime


def _get_control_set_by_name(session, name):
    try:
        return session.query(ControlSet).filter(ControlSet.name == name).one()
    except NoResultFound:
        print("No control set named " + name)
    return None


def new_lettuce_crop(session):
    germinate = _get_control_set_by_name(session, 'default germinate')
    seedlings = _get_control_set_by_name(session, 'default seedlings')
    main = _get_control_set_by_name(session, 'default main')
    if germinate is None or seedlings is None or main is None:
        return None
    else:
        now = datetime.now()
        seq_num = 0
        day_h = 12.0  # hours
        lettuce_crop = Crop(name='lettuce')
        session.add(lettuce_crop)
        session.commit()
        p1 = CropPhase(
                name='lettuce germination',
                control_set_id=germinate.id, crop_id=lettuce_crop.id,
                sequence=seq_num+1, duration_h=(day_h * 4.0))
        session.add(p1)
        p2 = CropPhase(
                name='lettuce seedlings',
                control_set_id=seedlings.id, crop_id=lettuce_crop.id,
                sequence=seq_num+1, duration_h=(day_h * 6.0))
        session.add(p2)
        p3 = CropPhase(
                name='lettuce main',
                control_set_id=main.id, crop_id=lettuce_crop.id,
                sequence=seq_num+1, duration_h=(day_h * 15.0))
        session.add(p3)
        session.commit()
        lettuce_crop.current_phase_id = p1.id
        lettuce_crop.current_phase_start = now
        lettuce_crop.sow_datetime = now
        session.add(lettuce_crop)
        session.commit()
        return lettuce_crop
