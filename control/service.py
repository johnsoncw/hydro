import time
import control.hydro


class Service():
    def __init__(self, crop_id):
        self.crop_id = crop_id
        print("Initializing control")

    def start(self):
        print("Starting control service")
        while True:
            time.sleep(3)
            control.hydro.adjust_outputs(self.crop_id)
            print("c")


def run_control(crop_id):
    server = Service(crop_id)
    server.start()
