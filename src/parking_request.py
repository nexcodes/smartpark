"""
ParkingRequest class - represents a parking request with state machine
"""
from datetime import datetime
from enums import RequestState


class ParkingRequest:
    """Represents a parking request with state management"""
    
    def __init__(self, request_id, vehicle_id, requested_zone):
        """
        Initialize a parking request
        
        Args:
            request_id: Unique identifier for the request
            vehicle_id: ID of the vehicle making the request
            requested_zone: Zone ID where parking is requested
        """
        self.request_id = request_id
        self.vehicle_id = vehicle_id
        self.requested_zone = requested_zone
        self.allocated_zone = None
        self.allocated_slot_id = None
        self.timestamp = datetime.now()
        self.current_state = RequestState.REQUESTED
        self.allocation_timestamp = None
        self.release_timestamp = None
    
    def change_state(self, new_state):
        """
        Change the state of the request with validation
        
        Args:
            new_state: New state to transition to
            
        Returns:
            bool: True if transition successful, False if invalid
        """
        if RequestState.is_valid_transition(self.current_state, new_state):
            self.current_state = new_state
            if new_state == RequestState.ALLOCATED:
                self.allocation_timestamp = datetime.now()
            elif new_state == RequestState.RELEASED:
                self.release_timestamp = datetime.now()
            return True
        else:
            print(f"Invalid state transition: {self.current_state.value} -> {new_state.value}")
            return False
    
    def allocate_slot(self, slot_id, zone_id):
        """
        Allocate a parking slot to this request
        
        Args:
            slot_id: ID of the allocated slot
            zone_id: Zone ID of the allocated slot
            
        Returns:
            bool: True if allocation successful
        """
        if self.change_state(RequestState.ALLOCATED):
            self.allocated_slot_id = slot_id
            self.allocated_zone = zone_id
            return True
        return False
    
    def get_parking_duration(self):
        """
        Calculate parking duration in seconds
        
        Returns:
            float: Duration in seconds, or None if not yet released
        """
        if self.allocation_timestamp and self.release_timestamp:
            duration = self.release_timestamp - self.allocation_timestamp
            return duration.total_seconds()
        return None
    
    def is_cross_zone_allocation(self):
        """Check if this is a cross-zone allocation (penalty case)"""
        return self.allocated_zone is not None and self.allocated_zone != self.requested_zone
    
    def __str__(self):
        return (f"Request {self.request_id}: Vehicle {self.vehicle_id}, "
                f"Zone {self.requested_zone}, State: {self.current_state.value}")
