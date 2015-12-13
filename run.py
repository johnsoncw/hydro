#!flask/bin/python
import time
# from web.server import HydroWebServer
from web.server import run_webserver
from monitor.service import run_monitor
import multiprocessing as mp

if __name__ == "__main__":
    pw = mp.Process(target=run_webserver)
    pw.start()
    pm = mp.Process(target=run_monitor)
    pm.start()
    # web_server = HydroWebServer()
    # web_server.start(debug=True)
    while True:
        time.sleep(5)
        print(".")
