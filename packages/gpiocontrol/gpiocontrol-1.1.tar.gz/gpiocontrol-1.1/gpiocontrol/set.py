import subprocess
from .state import State


def set(pin_number, state: State):
    if not 0 <= pin_number <= 27:
        raise Exception(f"ERROR: pin number {pin_number} out of range")
    command_result = subprocess.run(['/usr/bin/pinctrl', 'set', f'{pin_number}', 'op', state.set_arg()])
    if command_result.returncode != 0:
        raise Exception(f"ERROR: pin {pin_number} set: {command_result.stdout}")
