import input_output.interfaces
import input_output.simulated
import input_output.raspberry


def get_input_interface(sim=False):
    if sim:
        return simulated.SimulatedInput()
    return None


def get_output_interface(sim=False):
    if sim:
        return simulated.SimulatedOutput()
    return None
