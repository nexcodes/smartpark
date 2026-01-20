"""
Test suite for ParkingSlot class
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from parking_slot import ParkingSlot


class TestParkingSlot(unittest.TestCase):
    """Test cases for ParkingSlot class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.slot = ParkingSlot("ZONE-A-A1-1", "ZONE-A")
    
    def test_initialization(self):
        """Test slot initialization"""
        self.assertEqual(self.slot.slot_id, "ZONE-A-A1-1")
        self.assertEqual(self.slot.zone_id, "ZONE-A")
        self.assertTrue(self.slot.is_available)
        self.assertIsNone(self.slot.occupied_vehicle_id)
    
    def test_allocate_available_slot(self):
        """Test allocating an available slot"""
        result = self.slot.allocate("CAR-001")
        self.assertTrue(result)
        self.assertFalse(self.slot.is_available)
        self.assertEqual(self.slot.occupied_vehicle_id, "CAR-001")
    
    def test_allocate_occupied_slot(self):
        """Test allocating an already occupied slot"""
        self.slot.allocate("CAR-001")
        result = self.slot.allocate("CAR-002")
        self.assertFalse(result)
        self.assertEqual(self.slot.occupied_vehicle_id, "CAR-001")
    
    def test_release_occupied_slot(self):
        """Test releasing an occupied slot"""
        self.slot.allocate("CAR-001")
        vehicle_id = self.slot.release()
        self.assertEqual(vehicle_id, "CAR-001")
        self.assertTrue(self.slot.is_available)
        self.assertIsNone(self.slot.occupied_vehicle_id)
    
    def test_release_available_slot(self):
        """Test releasing an already available slot"""
        vehicle_id = self.slot.release()
        self.assertIsNone(vehicle_id)
        self.assertTrue(self.slot.is_available)
    
    def test_multiple_allocate_release_cycles(self):
        """Test multiple allocate-release cycles"""
        # First cycle
        self.slot.allocate("CAR-001")
        self.slot.release()
        
        # Second cycle
        result = self.slot.allocate("CAR-002")
        self.assertTrue(result)
        self.assertEqual(self.slot.occupied_vehicle_id, "CAR-002")
        
        # Third cycle
        self.slot.release()
        result = self.slot.allocate("CAR-003")
        self.assertTrue(result)
        self.assertEqual(self.slot.occupied_vehicle_id, "CAR-003")


if __name__ == '__main__':
    unittest.main()
