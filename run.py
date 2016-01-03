#!flask/bin/python
import time
# from web.server import HydroWebServer
from web.server import run_webserver
from monitor.service import run_monitor
from control.service import run_control
import multiprocessing as mp
from control.hydro import start_lettuce_crop
from database.hydro import get_db_session, get_current_crop

if __name__ == "__main__":
    pw = mp.Process(target=run_webserver)
    pw.start()
    pm = mp.Process(target=run_monitor)
    pm.start()
    pc = mp.Process(target=run_control)
    pc.start()
    time.sleep(5)
    session = get_db_session()
    crop = get_current_crop(session)
    if crop is None:
        start_lettuce_crop()
    # web_server = HydroWebServer()
    # web_server.start(debug=True)
    while True:
        time.sleep(5)
