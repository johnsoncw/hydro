import os
import input_output.interfaces
import input_output.simulated
import input_output.raspberry


def get_input_interface():
    if os.name == 'nt':
        return simulated.SimulatedInput()
    return None


def get_output_interface():
    if os.name == 'nt':
        return simulated.SimulatedOutput()
    return None
