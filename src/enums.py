"""
Enumerations for the Smart Parking System
"""
from enum import Enum


class RequestState(Enum):
    """State machine for parking requests"""
    REQUESTED = "REQUESTED"
    ALLOCATED = "ALLOCATED"
    OCCUPIED = "OCCUPIED"
    RELEASED = "RELEASED"
    CANCELLED = "CANCELLED"
    
    @staticmethod
    def is_valid_transition(from_state, to_state):
        """
        Validate state transitions
        Valid transitions:
        REQUESTED → ALLOCATED → OCCUPIED → RELEASED
        REQUESTED → CANCELLED
        ALLOCATED → CANCELLED
        """
        valid_transitions = {
            RequestState.REQUESTED: [RequestState.ALLOCATED, RequestState.CANCELLED],
            RequestState.ALLOCATED: [RequestState.OCCUPIED, RequestState.CANCELLED],
            RequestState.OCCUPIED: [RequestState.RELEASED],
            RequestState.RELEASED: [],
            RequestState.CANCELLED: []
        }
        
        return to_state in valid_transitions.get(from_state, [])
