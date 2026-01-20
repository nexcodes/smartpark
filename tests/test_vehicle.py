"""
Test suite for Vehicle class
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from vehicle import Vehicle


class TestVehicle(unittest.TestCase):
    """Test cases for Vehicle class"""
    
    def test_initialization_with_preferred_zone(self):
        """Test vehicle initialization with preferred zone"""
        vehicle = Vehicle("CAR-001", "ZONE-A")
        self.assertEqual(vehicle.vehicle_id, "CAR-001")
        self.assertEqual(vehicle.preferred_zone, "ZONE-A")
    
    def test_initialization_without_preferred_zone(self):
        """Test vehicle initialization without preferred zone"""
        vehicle = Vehicle("CAR-002", None)
        self.assertEqual(vehicle.vehicle_id, "CAR-002")
        self.assertIsNone(vehicle.preferred_zone)
    
    def test_multiple_vehicles(self):
        """Test creating multiple vehicles"""
        vehicles = [
            Vehicle("CAR-001", "ZONE-A"),
            Vehicle("CAR-002", "ZONE-B"),
            Vehicle("CAR-003", None)
        ]
        
        self.assertEqual(len(vehicles), 3)
        self.assertEqual(vehicles[0].vehicle_id, "CAR-001")
        self.assertEqual(vehicles[1].preferred_zone, "ZONE-B")
        self.assertIsNone(vehicles[2].preferred_zone)
    
    def test_vehicle_id_formats(self):
        """Test various vehicle ID formats"""
        v1 = Vehicle("CAR-001", "ZONE-A")
        v2 = Vehicle("TRUCK-XYZ", "ZONE-B")
        v3 = Vehicle("BIKE123", None)
        
        self.assertEqual(v1.vehicle_id, "CAR-001")
        self.assertEqual(v2.vehicle_id, "TRUCK-XYZ")
        self.assertEqual(v3.vehicle_id, "BIKE123")


if __name__ == '__main__':
    unittest.main()
