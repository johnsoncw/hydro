import time
import sys
import monitor.hydro


class Service():
    def __init__(self, crop_id):
        self.crop_id = crop_id
        print("Initializing monitor")

    def start(self):
        print("Starting monitor service")
        while True:
            time.sleep(30)
            monitor.hydro.take_measurements(self.crop_id)
            sys.stdout.write("m")
            sys.stdout.flush()


def run_monitor(crop_id):
    server = Service(crop_id)
    server.start()
