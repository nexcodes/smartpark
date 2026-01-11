"""
Vehicle class - represents a vehicle requesting parking
"""


class Vehicle:
    """Represents a vehicle in the parking system"""
    
    def __init__(self, vehicle_id, preferred_zone):
        """
        Initialize a vehicle
        
        Args:
            vehicle_id: Unique identifier for the vehicle
            preferred_zone: Zone ID where vehicle prefers to park
        """
        self.vehicle_id = vehicle_id
        self.preferred_zone = preferred_zone
    
    def __str__(self):
        return f"Vehicle {self.vehicle_id} (Prefers Zone {self.preferred_zone})"
