import time
import sys
import monitor.hydro


class Service():
    def __init__(self):
        print("Initializing monitor")

    def start(self):
        print("Starting monitor service")
        while True:
            time.sleep(5)
            monitor.hydro.take_measurements()
            sys.stdout.write("m")
            sys.stdout.flush()


def run_monitor():
    server = Service()
    server.start()
