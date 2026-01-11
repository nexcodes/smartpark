"""
Zone class - represents a parking zone containing multiple parking areas
"""
from parking_area import ParkingArea


class Zone:
    """Represents a zone containing multiple parking areas"""
    
    def __init__(self, zone_id):
        """
        Initialize a zone
        
        Args:
            zone_id: Unique identifier for the zone
        """
        self.zone_id = zone_id
        # Array of ParkingArea objects
        self.parking_areas = []
        # Custom adjacency list - array of zone IDs
        self.adjacent_zones = []
    
    def add_parking_area(self, area_id, capacity):
        """
        Add a parking area to this zone
        
        Args:
            area_id: Unique identifier for the parking area
            capacity: Number of parking slots in the area
        """
        area = ParkingArea(area_id, self.zone_id, capacity)
        self.parking_areas.append(area)
    
    def add_adjacent_zone(self, zone_id):
        """
        Add an adjacent zone to the adjacency list
        
        Args:
            zone_id: ID of the adjacent zone
        """
        if zone_id not in self.adjacent_zones:
            self.adjacent_zones.append(zone_id)
    
    def find_available_slot(self):
        """
        Find first available slot in this zone
        
        Returns:
            ParkingSlot: First available slot, or None if all occupied
        """
        for area in self.parking_areas:
            slot = area.find_available_slot()
            if slot:
                return slot
        return None
    
    def get_total_capacity(self):
        """Get total capacity of all parking areas in this zone"""
        total = 0
        for area in self.parking_areas:
            total += area.capacity
        return total
    
    def get_available_count(self):
        """Get count of available slots in this zone"""
        count = 0
        for area in self.parking_areas:
            count += area.get_available_count()
        return count
    
    def get_occupied_count(self):
        """Get count of occupied slots in this zone"""
        return self.get_total_capacity() - self.get_available_count()
    
    def __str__(self):
        available = self.get_available_count()
        total = self.get_total_capacity()
        return f"Zone {self.zone_id}: {available}/{total} available"
