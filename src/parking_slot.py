"""
ParkingSlot class - represents a single parking slot
"""


class ParkingSlot:
    """Represents a single parking slot in a parking area"""
    
    def __init__(self, slot_id, zone_id):
        """
        Initialize a parking slot
        
        Args:
            slot_id: Unique identifier for the slot
            zone_id: Zone where this slot is located
        """
        self.slot_id = slot_id
        self.zone_id = zone_id
        self.is_available = True
        self.occupied_vehicle_id = None
    
    def allocate(self, vehicle_id):
        """
        Allocate this slot to a vehicle
        
        Args:
            vehicle_id: ID of the vehicle to allocate to
            
        Returns:
            bool: True if allocation successful, False otherwise
        """
        if not self.is_available:
            return False
        
        self.is_available = False
        self.occupied_vehicle_id = vehicle_id
        return True
    
    def release(self):
        """
        Release this slot (make it available again)
        
        Returns:
            str: Vehicle ID that was occupying the slot, or None
        """
        vehicle_id = self.occupied_vehicle_id
        self.is_available = True
        self.occupied_vehicle_id = None
        return vehicle_id
    
    def __str__(self):
        status = "Available" if self.is_available else f"Occupied by {self.occupied_vehicle_id}"
        return f"Slot {self.slot_id} (Zone {self.zone_id}): {status}"
