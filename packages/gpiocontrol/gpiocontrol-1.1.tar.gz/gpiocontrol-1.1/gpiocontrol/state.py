from enum import Enum


class State(Enum):
    HIGH = 'hi'
    LOW = 'lo'

    def set_arg(self):
        match self:
            case State.HIGH:
                return 'dh'
            case State.LOW:
                return 'dl'
