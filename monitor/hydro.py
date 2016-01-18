import input_output
import database.core
import database.crops
import database.measurements


def take_measurements(crop_id):
    session = database.core.get_db_session()
    crop = database.crops.get_crop_by_id(session, crop_id)
    ext_ip = input_output.get_input_interface(crop.simulated)
    database.measurements.store_measurement(
        session,
        crop,
        ext_ip)
