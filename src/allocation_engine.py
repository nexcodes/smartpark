"""
AllocationEngine - handles parking slot allocation logic
"""
from enums import RequestState


class AllocationEngine:
    """Handles parking slot allocation with same-zone priority and cross-zone fallback"""
    
    def __init__(self, zones):
        """
        Initialize the allocation engine
        
        Args:
            zones: Dictionary of zone_id -> Zone objects
        """
        self.zones = zones
    
    def allocate_slot(self, parking_request):
        """
        Allocate a parking slot for a request
        
        Priority:
        1. Try same-zone allocation first
        2. Try adjacent zones with penalty
        3. Try any available zone with penalty
        
        Args:
            parking_request: ParkingRequest object
            
        Returns:
            dict: Allocation result with status, slot_id, zone_id, and penalty
        """
        if parking_request.current_state != RequestState.REQUESTED:
            return {
                'success': False,
                'message': f"Cannot allocate - request is in {parking_request.current_state.value} state",
                'penalty': 0
            }
        
        requested_zone_id = parking_request.requested_zone
        
        # Step 1: Try same-zone allocation (no penalty)
        if requested_zone_id in self.zones:
            zone = self.zones[requested_zone_id]
            slot = zone.find_available_slot()
            
            if slot:
                # Allocate the slot
                if slot.allocate(parking_request.vehicle_id):
                    parking_request.allocate_slot(slot.slot_id, zone.zone_id)
                    return {
                        'success': True,
                        'slot_id': slot.slot_id,
                        'zone_id': zone.zone_id,
                        'penalty': 0,
                        'message': 'Allocated in requested zone'
                    }
        
        # Step 2: Try adjacent zones (with penalty)
        if requested_zone_id in self.zones:
            zone = self.zones[requested_zone_id]
            for adjacent_zone_id in zone.adjacent_zones:
                if adjacent_zone_id in self.zones:
                    adj_zone = self.zones[adjacent_zone_id]
                    slot = adj_zone.find_available_slot()
                    
                    if slot:
                        if slot.allocate(parking_request.vehicle_id):
                            parking_request.allocate_slot(slot.slot_id, adj_zone.zone_id)
                            return {
                                'success': True,
                                'slot_id': slot.slot_id,
                                'zone_id': adj_zone.zone_id,
                                'penalty': 50,  # Penalty for adjacent zone
                                'message': f'Allocated in adjacent zone {adj_zone.zone_id}'
                            }
        
        # Step 3: Try any available zone (with higher penalty)
        for zone_id, zone in self.zones.items():
            if zone_id != requested_zone_id:
                slot = zone.find_available_slot()
                
                if slot:
                    if slot.allocate(parking_request.vehicle_id):
                        parking_request.allocate_slot(slot.slot_id, zone.zone_id)
                        return {
                            'success': True,
                            'slot_id': slot.slot_id,
                            'zone_id': zone.zone_id,
                            'penalty': 100,  # Higher penalty for non-adjacent zone
                            'message': f'Allocated in distant zone {zone.zone_id}'
                        }
        
        # No slots available anywhere
        return {
            'success': False,
            'message': 'No available slots in any zone',
            'penalty': 0
        }
    
    def cancel_request(self, parking_request):
        """
        Cancel a parking request and release any allocated slot
        
        Args:
            parking_request: ParkingRequest object
            
        Returns:
            dict: Result with success status and message
        """
        current_state = parking_request.current_state
        
        # Can only cancel from REQUESTED or ALLOCATED states
        if current_state not in [RequestState.REQUESTED, RequestState.ALLOCATED]:
            return {
                'success': False,
                'message': f'Cannot cancel - request is in {current_state.value} state'
            }
        
        # If allocated, release the slot
        if current_state == RequestState.ALLOCATED and parking_request.allocated_slot_id:
            # Find and release the slot
            slot = self._find_slot(parking_request.allocated_slot_id)
            if slot:
                slot.release()
        
        # Change state to CANCELLED
        parking_request.change_state(RequestState.CANCELLED)
        
        return {
            'success': True,
            'message': f'Request cancelled from {current_state.value} state'
        }
    
    def release_parking(self, parking_request):
        """
        Release parking (vehicle leaving)
        
        Args:
            parking_request: ParkingRequest object
            
        Returns:
            dict: Result with success status and message
        """
        if parking_request.current_state != RequestState.OCCUPIED:
            return {
                'success': False,
                'message': f'Cannot release - request is in {parking_request.current_state.value} state'
            }
        
        # Find and release the slot
        slot = self._find_slot(parking_request.allocated_slot_id)
        if slot:
            slot.release()
        
        # Change state to RELEASED
        parking_request.change_state(RequestState.RELEASED)
        
        return {
            'success': True,
            'message': 'Parking released successfully'
        }
    
    def _find_slot(self, slot_id):
        """
        Find a slot by its ID
        
        Args:
            slot_id: Slot ID to search for
            
        Returns:
            ParkingSlot: Slot object or None if not found
        """
        for zone in self.zones.values():
            for area in zone.parking_areas:
                for slot in area.slots:
                    if slot.slot_id == slot_id:
                        return slot
        return None
