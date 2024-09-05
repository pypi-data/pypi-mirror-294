import subprocess
from .state import State


def get(pin_number):
    command_result = subprocess.run(['/usr/bin/pinctrl', 'get', f'{pin_number}'],
                                    capture_output=True)
    if command_result.returncode != 0:
        raise Exception(f"ERROR: pin {pin_number} get: {command_result.stdout}")
    return State(command_result.stdout.decode('utf-8').strip().split('|')[1].strip().split()[0])
