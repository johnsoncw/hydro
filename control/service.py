import time
import control.hydro


class Service():
    def __init__(self):
        print("Initializing control")

    def start(self):
        print("Starting control service")
        while True:
            time.sleep(30)
            control.hydro.adjust_outputs()
            print("c")


def run_control():
    server = Service()
    server.start()
