"""
Test suite for ParkingArea class
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from parking_area import ParkingArea


class TestParkingArea(unittest.TestCase):
    """Test cases for ParkingArea class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.area = ParkingArea("A1", "ZONE-A", 5)
    
    def test_initialization(self):
        """Test parking area initialization"""
        self.assertEqual(self.area.area_id, "A1")
        self.assertEqual(self.area.zone_id, "ZONE-A")
        self.assertEqual(self.area.capacity, 5)
        self.assertEqual(len(self.area.slots), 5)
    
    def test_slot_ids_format(self):
        """Test that slots are created with correct ID format"""
        for i, slot in enumerate(self.area.slots, 1):
            expected_id = f"ZONE-A-A1-{i}"
            self.assertEqual(slot.slot_id, expected_id)
            self.assertEqual(slot.zone_id, "ZONE-A")
    
    def test_find_available_slot_all_available(self):
        """Test finding available slot when all are available"""
        slot = self.area.find_available_slot()
        self.assertIsNotNone(slot)
        self.assertTrue(slot.is_available)
        self.assertEqual(slot.slot_id, "ZONE-A-A1-1")  # Should return first
    
    def test_find_available_slot_some_occupied(self):
        """Test finding available slot when some are occupied"""
        # Occupy first 2 slots
        self.area.slots[0].allocate("CAR-001")
        self.area.slots[1].allocate("CAR-002")
        
        slot = self.area.find_available_slot()
        self.assertIsNotNone(slot)
        self.assertEqual(slot.slot_id, "ZONE-A-A1-3")  # Should return third
    
    def test_find_available_slot_all_occupied(self):
        """Test finding available slot when all are occupied"""
        # Occupy all slots
        for i, slot in enumerate(self.area.slots, 1):
            slot.allocate(f"CAR-{i:03d}")
        
        slot = self.area.find_available_slot()
        self.assertIsNone(slot)
    
    def test_get_available_count_all_available(self):
        """Test available count when all slots are free"""
        count = self.area.get_available_count()
        self.assertEqual(count, 5)
    
    def test_get_available_count_some_occupied(self):
        """Test available count when some slots are occupied"""
        self.area.slots[0].allocate("CAR-001")
        self.area.slots[2].allocate("CAR-002")
        
        count = self.area.get_available_count()
        self.assertEqual(count, 3)
    
    def test_get_available_count_all_occupied(self):
        """Test available count when all slots are occupied"""
        for i, slot in enumerate(self.area.slots, 1):
            slot.allocate(f"CAR-{i:03d}")
        
        count = self.area.get_available_count()
        self.assertEqual(count, 0)
    
    def test_get_occupied_count_none_occupied(self):
        """Test occupied count when no slots are occupied"""
        count = self.area.get_occupied_count()
        self.assertEqual(count, 0)
    
    def test_get_occupied_count_some_occupied(self):
        """Test occupied count when some slots are occupied"""
        self.area.slots[1].allocate("CAR-001")
        self.area.slots[3].allocate("CAR-002")
        
        count = self.area.get_occupied_count()
        self.assertEqual(count, 2)
    
    def test_get_occupied_count_all_occupied(self):
        """Test occupied count when all slots are occupied"""
        for i, slot in enumerate(self.area.slots, 1):
            slot.allocate(f"CAR-{i:03d}")
        
        count = self.area.get_occupied_count()
        self.assertEqual(count, 5)
    
    def test_available_and_occupied_counts_sum(self):
        """Test that available + occupied = capacity"""
        # Occupy random slots
        self.area.slots[0].allocate("CAR-001")
        self.area.slots[3].allocate("CAR-002")
        
        available = self.area.get_available_count()
        occupied = self.area.get_occupied_count()
        
        self.assertEqual(available + occupied, self.area.capacity)
    
    def test_large_capacity_area(self):
        """Test parking area with large capacity"""
        large_area = ParkingArea("B1", "ZONE-B", 50)
        self.assertEqual(large_area.capacity, 50)
        self.assertEqual(len(large_area.slots), 50)
        self.assertEqual(large_area.get_available_count(), 50)


if __name__ == '__main__':
    unittest.main()
