"""
ParkingArea class - represents a collection of parking slots
"""
from parking_slot import ParkingSlot


class ParkingArea:
    """Represents a parking area containing multiple parking slots"""
    
    def __init__(self, area_id, zone_id, capacity):
        """
        Initialize a parking area
        
        Args:
            area_id: Unique identifier for the parking area
            zone_id: Zone where this area is located
            capacity: Number of parking slots in this area
        """
        self.area_id = area_id
        self.zone_id = zone_id
        self.capacity = capacity
        # Array of ParkingSlot objects
        self.slots = []
        
        # Create parking slots
        for i in range(capacity):
            slot_id = f"{zone_id}-{area_id}-{i+1}"
            self.slots.append(ParkingSlot(slot_id, zone_id))
    
    def find_available_slot(self):
        """
        Find the first available parking slot
        
        Returns:
            ParkingSlot: First available slot, or None if all occupied
        """
        for slot in self.slots:
            if slot.is_available:
                return slot
        return None
    
    def get_available_count(self):
        """Get count of available slots"""
        count = 0
        for slot in self.slots:
            if slot.is_available:
                count += 1
        return count
    
    def get_occupied_count(self):
        """Get count of occupied slots"""
        return self.capacity - self.get_available_count()
    
    def __str__(self):
        available = self.get_available_count()
        return f"Area {self.area_id} (Zone {self.zone_id}): {available}/{self.capacity} available"
