"""
Test suite for Zone class
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from zone import Zone


class TestZone(unittest.TestCase):
    """Test cases for Zone class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.zone = Zone("ZONE-A")
    
    def test_initialization(self):
        """Test zone initialization"""
        self.assertEqual(self.zone.zone_id, "ZONE-A")
        self.assertEqual(len(self.zone.parking_areas), 0)
        self.assertEqual(len(self.zone.adjacent_zones), 0)
    
    def test_add_parking_area(self):
        """Test adding parking area to zone"""
        self.zone.add_parking_area("A1", 10)
        
        self.assertEqual(len(self.zone.parking_areas), 1)
        self.assertEqual(self.zone.parking_areas[0].area_id, "A1")
        self.assertEqual(self.zone.parking_areas[0].capacity, 10)
    
    def test_add_multiple_parking_areas(self):
        """Test adding multiple parking areas"""
        self.zone.add_parking_area("A1", 10)
        self.zone.add_parking_area("A2", 15)
        self.zone.add_parking_area("A3", 5)
        
        self.assertEqual(len(self.zone.parking_areas), 3)
        self.assertEqual(self.zone.parking_areas[0].area_id, "A1")
        self.assertEqual(self.zone.parking_areas[1].area_id, "A2")
        self.assertEqual(self.zone.parking_areas[2].area_id, "A3")
    
    def test_add_adjacent_zone(self):
        """Test adding adjacent zone"""
        self.zone.add_adjacent_zone("ZONE-B")
        
        self.assertEqual(len(self.zone.adjacent_zones), 1)
        self.assertIn("ZONE-B", self.zone.adjacent_zones)
    
    def test_add_multiple_adjacent_zones(self):
        """Test adding multiple adjacent zones"""
        self.zone.add_adjacent_zone("ZONE-B")
        self.zone.add_adjacent_zone("ZONE-C")
        self.zone.add_adjacent_zone("ZONE-D")
        
        self.assertEqual(len(self.zone.adjacent_zones), 3)
        self.assertIn("ZONE-B", self.zone.adjacent_zones)
        self.assertIn("ZONE-C", self.zone.adjacent_zones)
        self.assertIn("ZONE-D", self.zone.adjacent_zones)
    
    def test_find_available_slot_empty_zone(self):
        """Test finding available slot in zone with no areas"""
        slot = self.zone.find_available_slot()
        self.assertIsNone(slot)
    
    def test_find_available_slot_all_available(self):
        """Test finding available slot when slots are available"""
        self.zone.add_parking_area("A1", 5)
        self.zone.add_parking_area("A2", 3)
        
        slot = self.zone.find_available_slot()
        self.assertIsNotNone(slot)
        self.assertTrue(slot.is_available)
    
    def test_find_available_slot_first_area_full(self):
        """Test finding available slot when first area is full"""
        self.zone.add_parking_area("A1", 2)
        self.zone.add_parking_area("A2", 3)
        
        # Fill first area
        for slot in self.zone.parking_areas[0].slots:
            slot.allocate(f"CAR-{slot.slot_id}")
        
        slot = self.zone.find_available_slot()
        self.assertIsNotNone(slot)
        # Should return slot from second area
        self.assertTrue(slot.slot_id.startswith("ZONE-A-A2"))
    
    def test_find_available_slot_all_occupied(self):
        """Test finding available slot when all are occupied"""
        self.zone.add_parking_area("A1", 2)
        
        # Occupy all slots
        for area in self.zone.parking_areas:
            for slot in area.slots:
                slot.allocate(f"CAR-{slot.slot_id}")
        
        slot = self.zone.find_available_slot()
        self.assertIsNone(slot)
    
    def test_get_total_capacity_empty_zone(self):
        """Test total capacity of empty zone"""
        capacity = self.zone.get_total_capacity()
        self.assertEqual(capacity, 0)
    
    def test_get_total_capacity_single_area(self):
        """Test total capacity with single area"""
        self.zone.add_parking_area("A1", 10)
        capacity = self.zone.get_total_capacity()
        self.assertEqual(capacity, 10)
    
    def test_get_total_capacity_multiple_areas(self):
        """Test total capacity with multiple areas"""
        self.zone.add_parking_area("A1", 10)
        self.zone.add_parking_area("A2", 15)
        self.zone.add_parking_area("A3", 5)
        
        capacity = self.zone.get_total_capacity()
        self.assertEqual(capacity, 30)
    
    def test_get_available_count_all_available(self):
        """Test available count when all slots are free"""
        self.zone.add_parking_area("A1", 5)
        self.zone.add_parking_area("A2", 3)
        
        count = self.zone.get_available_count()
        self.assertEqual(count, 8)
    
    def test_get_available_count_some_occupied(self):
        """Test available count when some slots are occupied"""
        self.zone.add_parking_area("A1", 5)
        self.zone.add_parking_area("A2", 3)
        
        # Occupy 3 slots
        self.zone.parking_areas[0].slots[0].allocate("CAR-001")
        self.zone.parking_areas[0].slots[2].allocate("CAR-002")
        self.zone.parking_areas[1].slots[1].allocate("CAR-003")
        
        count = self.zone.get_available_count()
        self.assertEqual(count, 5)
    
    def test_get_occupied_count_none_occupied(self):
        """Test occupied count when no slots are occupied"""
        self.zone.add_parking_area("A1", 5)
        
        count = self.zone.get_occupied_count()
        self.assertEqual(count, 0)
    
    def test_get_occupied_count_some_occupied(self):
        """Test occupied count when some slots are occupied"""
        self.zone.add_parking_area("A1", 5)
        self.zone.add_parking_area("A2", 3)
        
        # Occupy 4 slots
        self.zone.parking_areas[0].slots[0].allocate("CAR-001")
        self.zone.parking_areas[0].slots[1].allocate("CAR-002")
        self.zone.parking_areas[1].slots[0].allocate("CAR-003")
        self.zone.parking_areas[1].slots[2].allocate("CAR-004")
        
        count = self.zone.get_occupied_count()
        self.assertEqual(count, 4)
    
    def test_available_and_occupied_sum_to_capacity(self):
        """Test that available + occupied = total capacity"""
        self.zone.add_parking_area("A1", 10)
        self.zone.add_parking_area("A2", 5)
        
        # Occupy some slots
        self.zone.parking_areas[0].slots[0].allocate("CAR-001")
        self.zone.parking_areas[1].slots[1].allocate("CAR-002")
        
        available = self.zone.get_available_count()
        occupied = self.zone.get_occupied_count()
        total = self.zone.get_total_capacity()
        
        self.assertEqual(available + occupied, total)


if __name__ == '__main__':
    unittest.main()
