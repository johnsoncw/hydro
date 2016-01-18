import time
import multiprocessing as mp

import database.crops
import monitor.service
import web.server
import control.service

if __name__ == "__main__":
    crop_id = database.crops.get_crop_id("emma_lettuce_1", simulated=True, create=True)
    if crop_id:
        pw = mp.Process(target=web.server.run_webserver, args=(crop_id,))
        pw.start()
        pm = mp.Process(target=monitor.service.run_monitor, args=(crop_id,))
        pm.start()
        pc = mp.Process(target=control.service.run_control, args=(crop_id,))
        pc.start()
        while True:
            time.sleep(5)
