"""
Test module for ParkingSystem class
Tests comprehensive system operations including zone management, requests, and state transitions
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from parking_system import ParkingSystem
from enums import RequestState


class TestParkingSystem(unittest.TestCase):
    """Test cases for ParkingSystem class"""
    
    def setUp(self):
        """Set up test fixtures before each test"""
        self.system = ParkingSystem()
        
    def test_initial_state(self):
        """Test initial state of parking system"""
        self.assertEqual(len(self.system.zones), 0)
        self.assertEqual(len(self.system.vehicles), 0)
        self.assertEqual(len(self.system.requests), 0)
        self.assertEqual(self.system.next_request_id, 1)
        
    def test_add_zone_success(self):
        """Test successful zone addition"""
        result = self.system.add_zone("ZONE-A", "Premium Zone")
        self.assertTrue(result['success'])
        self.assertIn("ZONE-A", self.system.zones)
        self.assertEqual(self.system.zones["ZONE-A"].zone_id, "ZONE-A")
        
    def test_add_zone_duplicate(self):
        """Test adding duplicate zone"""
        self.system.add_zone("ZONE-A", "Zone A")
        result = self.system.add_zone("ZONE-A", "Zone A Duplicate")
        self.assertFalse(result['success'])
        self.assertIn("already exists", result['message'].lower())
        
    def test_add_zone_empty_id(self):
        """Test adding zone with empty ID"""
        result = self.system.add_zone("", "Empty Zone")
        self.assertFalse(result['success'])
        
    def test_link_adjacent_zones_success(self):
        """Test successful zone linking"""
        self.system.add_zone("ZONE-A", "Zone A")
        self.system.add_zone("ZONE-B", "Zone B")
        result = self.system.link_adjacent_zones("ZONE-A", "ZONE-B")
        self.assertTrue(result['success'])
        self.assertIn("ZONE-B", self.system.zones["ZONE-A"].adjacent_zones)
        self.assertIn("ZONE-A", self.system.zones["ZONE-B"].adjacent_zones)
        
    def test_link_adjacent_zones_nonexistent(self):
        """Test linking non-existent zones"""
        self.system.add_zone("ZONE-A", "Zone A")
        result = self.system.link_adjacent_zones("ZONE-A", "ZONE-X")
        self.assertFalse(result['success'])
        
    def test_link_zone_to_itself(self):
        """Test linking zone to itself"""
        self.system.add_zone("ZONE-A", "Zone A")
        result = self.system.link_adjacent_zones("ZONE-A", "ZONE-A")
        self.assertFalse(result['success'])
        
    def test_add_parking_area_success(self):
        """Test successful parking area addition"""
        self.system.add_zone("ZONE-A", "Zone A")
        result = self.system.add_parking_area("ZONE-A", "AREA-1", 10)
        self.assertTrue(result['success'])
        self.assertEqual(len(self.system.zones["ZONE-A"].areas), 1)
        
    def test_add_parking_area_nonexistent_zone(self):
        """Test adding area to non-existent zone"""
        result = self.system.add_parking_area("ZONE-X", "AREA-1", 10)
        self.assertFalse(result['success'])
        
    def test_add_parking_area_invalid_capacity(self):
        """Test adding area with invalid capacity"""
        self.system.add_zone("ZONE-A", "Zone A")
        result = self.system.add_parking_area("ZONE-A", "AREA-1", 0)
        self.assertFalse(result['success'])
        
    def test_register_vehicle_success(self):
        """Test successful vehicle registration"""
        result = self.system.register_vehicle("CAR-001", "ZONE-A")
        self.assertTrue(result['success'])
        self.assertIn("CAR-001", self.system.vehicles)
        self.assertEqual(self.system.vehicles["CAR-001"].preferred_zone, "ZONE-A")
        
    def test_register_vehicle_duplicate(self):
        """Test registering duplicate vehicle"""
        self.system.register_vehicle("CAR-001", "ZONE-A")
        result = self.system.register_vehicle("CAR-001", "ZONE-A")
        self.assertFalse(result['success'])
        
    def test_register_vehicle_empty_id(self):
        """Test registering vehicle with empty ID"""
        result = self.system.register_vehicle("", "ZONE-A")
        self.assertFalse(result['success'])
        
    def test_create_parking_request_success(self):
        """Test successful parking request creation"""
        self.system.add_zone("ZONE-A", "Zone A")
        self.system.add_parking_area("ZONE-A", "AREA-1", 10)
        self.system.register_vehicle("CAR-001", "ZONE-A")
        
        result = self.system.create_parking_request("CAR-001", "ZONE-A")
        self.assertTrue(result['success'])
        self.assertIn('request_id', result)
        self.assertEqual(self.system.requests[result['request_id']].vehicle_id, "CAR-001")
        
    def test_create_parking_request_nonexistent_vehicle(self):
        """Test creating request for non-existent vehicle"""
        self.system.add_zone("ZONE-A", "Zone A")
        result = self.system.create_parking_request("CAR-999", "ZONE-A")
        self.assertFalse(result['success'])
        
    def test_create_parking_request_nonexistent_zone(self):
        """Test creating request for non-existent zone"""
        self.system.register_vehicle("CAR-001", "ZONE-A")
        result = self.system.create_parking_request("CAR-001", "ZONE-X")
        self.assertFalse(result['success'])
        
    def test_allocate_slot_success(self):
        """Test successful slot allocation"""
        self.system.add_zone("ZONE-A", "Zone A")
        self.system.add_parking_area("ZONE-A", "AREA-1", 10)
        self.system.register_vehicle("CAR-001", "ZONE-A")
        req_result = self.system.create_parking_request("CAR-001", "ZONE-A")
        request_id = req_result['request_id']
        
        result = self.system.allocate_slot(request_id)
        self.assertTrue(result['success'])
        self.assertIn('slot_id', result)
        self.assertEqual(self.system.requests[request_id].current_state, RequestState.ALLOCATED)
        
    def test_allocate_slot_nonexistent_request(self):
        """Test allocating slot for non-existent request"""
        result = self.system.allocate_slot(999)
        self.assertFalse(result['success'])
        
    def test_allocate_slot_no_available_slots(self):
        """Test allocation when no slots available"""
        self.system.add_zone("ZONE-A", "Zone A")
        self.system.add_parking_area("ZONE-A", "AREA-1", 1)
        self.system.register_vehicle("CAR-001", "ZONE-A")
        self.system.register_vehicle("CAR-002", "ZONE-A")
        
        # Allocate first slot
        req1 = self.system.create_parking_request("CAR-001", "ZONE-A")
        self.system.allocate_slot(req1['request_id'])
        
        # Try to allocate second when no slots available
        req2 = self.system.create_parking_request("CAR-002", "ZONE-A")
        result = self.system.allocate_slot(req2['request_id'])
        self.assertFalse(result['success'])
        
    def test_occupy_slot_success(self):
        """Test successful slot occupation"""
        self.system.add_zone("ZONE-A", "Zone A")
        self.system.add_parking_area("ZONE-A", "AREA-1", 10)
        self.system.register_vehicle("CAR-001", "ZONE-A")
        req = self.system.create_parking_request("CAR-001", "ZONE-A")
        self.system.allocate_slot(req['request_id'])
        
        result = self.system.occupy_slot(req['request_id'])
        self.assertTrue(result['success'])
        self.assertEqual(self.system.requests[req['request_id']].current_state, RequestState.OCCUPIED)
        
    def test_occupy_slot_not_allocated(self):
        """Test occupying slot without allocation"""
        self.system.add_zone("ZONE-A", "Zone A")
        self.system.add_parking_area("ZONE-A", "AREA-1", 10)
        self.system.register_vehicle("CAR-001", "ZONE-A")
        req = self.system.create_parking_request("CAR-001", "ZONE-A")
        
        result = self.system.occupy_slot(req['request_id'])
        self.assertFalse(result['success'])
        
    def test_release_slot_success(self):
        """Test successful slot release"""
        self.system.add_zone("ZONE-A", "Zone A")
        self.system.add_parking_area("ZONE-A", "AREA-1", 10)
        self.system.register_vehicle("CAR-001", "ZONE-A")
        req = self.system.create_parking_request("CAR-001", "ZONE-A")
        self.system.allocate_slot(req['request_id'])
        self.system.occupy_slot(req['request_id'])
        
        result = self.system.release_slot(req['request_id'])
        self.assertTrue(result['success'])
        self.assertEqual(self.system.requests[req['request_id']].current_state, RequestState.RELEASED)
        
    def test_cancel_request_success(self):
        """Test successful request cancellation"""
        self.system.add_zone("ZONE-A", "Zone A")
        self.system.add_parking_area("ZONE-A", "AREA-1", 10)
        self.system.register_vehicle("CAR-001", "ZONE-A")
        req = self.system.create_parking_request("CAR-001", "ZONE-A")
        
        result = self.system.cancel_request(req['request_id'])
        self.assertTrue(result['success'])
        self.assertEqual(self.system.requests[req['request_id']].current_state, RequestState.CANCELLED)
        
    def test_allocation_with_adjacent_zones(self):
        """Test allocation tries adjacent zones when preferred zone is full"""
        self.system.add_zone("ZONE-A", "Zone A")
        self.system.add_zone("ZONE-B", "Zone B")
        self.system.link_adjacent_zones("ZONE-A", "ZONE-B")
        self.system.add_parking_area("ZONE-A", "AREA-1", 1)
        self.system.add_parking_area("ZONE-B", "AREA-1", 10)
        
        self.system.register_vehicle("CAR-001", "ZONE-A")
        self.system.register_vehicle("CAR-002", "ZONE-A")
        
        # Fill ZONE-A
        req1 = self.system.create_parking_request("CAR-001", "ZONE-A")
        self.system.allocate_slot(req1['request_id'])
        
        # Request ZONE-A but should get ZONE-B with penalty
        req2 = self.system.create_parking_request("CAR-002", "ZONE-A")
        result = self.system.allocate_slot(req2['request_id'])
        self.assertTrue(result['success'])
        self.assertEqual(result['penalty'], 50)
        
    def test_get_zone_status(self):
        """Test retrieving zone status"""
        self.system.add_zone("ZONE-A", "Zone A")
        self.system.add_parking_area("ZONE-A", "AREA-1", 10)
        
        result = self.system.get_zone_status("ZONE-A")
        self.assertTrue(result['success'])
        self.assertEqual(result['total_slots'], 10)
        self.assertEqual(result['available_slots'], 10)
        
    def test_get_all_zones_summary(self):
        """Test retrieving all zones summary"""
        self.system.add_zone("ZONE-A", "Zone A")
        self.system.add_zone("ZONE-B", "Zone B")
        self.system.add_parking_area("ZONE-A", "AREA-1", 10)
        self.system.add_parking_area("ZONE-B", "AREA-1", 5)
        
        result = self.system.get_all_zones_summary()
        self.assertTrue(result['success'])
        self.assertEqual(len(result['zones']), 2)
        
    def test_get_request_details(self):
        """Test retrieving request details"""
        self.system.add_zone("ZONE-A", "Zone A")
        self.system.add_parking_area("ZONE-A", "AREA-1", 10)
        self.system.register_vehicle("CAR-001", "ZONE-A")
        req = self.system.create_parking_request("CAR-001", "ZONE-A")
        
        result = self.system.get_request_details(req['request_id'])
        self.assertTrue(result['success'])
        self.assertEqual(result['vehicle_id'], "CAR-001")
        self.assertEqual(result['current_state'], 'REQUESTED')
        
    def test_list_all_requests(self):
        """Test listing all requests"""
        self.system.add_zone("ZONE-A", "Zone A")
        self.system.add_parking_area("ZONE-A", "AREA-1", 10)
        self.system.register_vehicle("CAR-001", "ZONE-A")
        self.system.register_vehicle("CAR-002", "ZONE-A")
        
        self.system.create_parking_request("CAR-001", "ZONE-A")
        self.system.create_parking_request("CAR-002", "ZONE-A")
        
        result = self.system.list_all_requests()
        self.assertTrue(result['success'])
        self.assertEqual(len(result['requests']), 2)


if __name__ == '__main__':
    unittest.main()
