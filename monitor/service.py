import time


class Service():
    def __init__(self):
        print("Initializing monitor")

    def start(self):
        print("Starting monitor service")
        while True:
            time.sleep(5)
            print("m")


def run_monitor():
    server = Service()
    server.start()
