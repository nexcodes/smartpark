"""
Test module for Analytics class
Tests metrics calculation, occupancy tracking, and report generation
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from datetime import datetime, timedelta
from parking_system import ParkingSystem
from analytics import Analytics


class TestAnalytics(unittest.TestCase):
    """Test cases for Analytics class"""
    
    def setUp(self):
        """Set up test fixtures before each test"""
        self.system = ParkingSystem()
        self.analytics = Analytics(self.system)
        
        # Setup basic infrastructure
        self.system.add_zone("ZONE-A", "Zone A")
        self.system.add_parking_area("ZONE-A", "AREA-1", 10)
        
    def test_initial_metrics(self):
        """Test initial analytics metrics"""
        result = self.analytics.get_overall_metrics()
        
        self.assertTrue(result['success'])
        self.assertEqual(result['total_requests'], 0)
        self.assertEqual(result['allocated_requests'], 0)
        self.assertEqual(result['cancelled_requests'], 0)
        self.assertEqual(result['released_requests'], 0)
        
    def test_total_requests_count(self):
        """Test counting total requests"""
        self.system.register_vehicle("CAR-001", VehicleType.CAR, "John Doe")
        self.system.register_vehicle("CAR-002", VehicleType.CAR, "Jane Doe")
        
        self.system.create_parking_request("CAR-001", "ZONE-A")
        self.system.create_parking_request("CAR-002", "ZONE-A")
        
        result = self.analytics.get_overall_metrics()
        self.assertEqual(result['total_requests'], 2)
        
    def test_allocated_requests_count(self):
        """Test counting allocated requests"""
        self.system.register_vehicle("CAR-001", VehicleType.CAR, "John Doe")
        req = self.system.create_parking_request("CAR-001", "ZONE-A")
        self.system.allocate_slot(req['request_id'])
        
        result = self.analytics.get_overall_metrics()
        self.assertEqual(result['allocated_requests'], 1)
        
    def test_cancelled_requests_count(self):
        """Test counting cancelled requests"""
        self.system.register_vehicle("CAR-001", VehicleType.CAR, "John Doe")
        req = self.system.create_parking_request("CAR-001", "ZONE-A")
        self.system.cancel_request(req['request_id'])
        
        result = self.analytics.get_overall_metrics()
        self.assertEqual(result['cancelled_requests'], 1)
        
    def test_released_requests_count(self):
        """Test counting released requests"""
        self.system.register_vehicle("CAR-001", VehicleType.CAR, "John Doe")
        req = self.system.create_parking_request("CAR-001", "ZONE-A")
        self.system.allocate_slot(req['request_id'])
        self.system.occupy_slot(req['request_id'])
        self.system.release_slot(req['request_id'])
        
        result = self.analytics.get_overall_metrics()
        self.assertEqual(result['released_requests'], 1)
        
    def test_occupancy_rate_empty(self):
        """Test occupancy rate when no slots occupied"""
        result = self.analytics.get_overall_metrics()
        self.assertEqual(result['occupancy_rate'], 0.0)
        
    def test_occupancy_rate_partial(self):
        """Test occupancy rate with partial occupation"""
        self.system.register_vehicle("CAR-001", VehicleType.CAR, "John Doe")
        self.system.register_vehicle("CAR-002", VehicleType.CAR, "Jane Doe")
        
        req1 = self.system.create_parking_request("CAR-001", "ZONE-A")
        self.system.allocate_slot(req1['request_id'])
        self.system.occupy_slot(req1['request_id'])
        
        req2 = self.system.create_parking_request("CAR-002", "ZONE-A")
        self.system.allocate_slot(req2['request_id'])
        self.system.occupy_slot(req2['request_id'])
        
        result = self.analytics.get_overall_metrics()
        self.assertEqual(result['occupancy_rate'], 20.0)  # 2/10 = 20%
        
    def test_occupancy_rate_full(self):
        """Test occupancy rate when fully occupied"""
        # Create a small zone
        self.system.add_zone("ZONE-B", "Zone B")
        self.system.add_parking_area("ZONE-B", "AREA-1", 2)
        
        self.system.register_vehicle("CAR-001", VehicleType.CAR, "John Doe")
        self.system.register_vehicle("CAR-002", VehicleType.CAR, "Jane Doe")
        
        req1 = self.system.create_parking_request("CAR-001", "ZONE-B")
        self.system.allocate_slot(req1['request_id'])
        self.system.occupy_slot(req1['request_id'])
        
        req2 = self.system.create_parking_request("CAR-002", "ZONE-B")
        self.system.allocate_slot(req2['request_id'])
        self.system.occupy_slot(req2['request_id'])
        
        result = self.analytics.get_zone_metrics("ZONE-B")
        self.assertEqual(result['occupancy_rate'], 100.0)
        
    def test_zone_metrics(self):
        """Test zone-specific metrics"""
        self.system.register_vehicle("CAR-001", VehicleType.CAR, "John Doe")
        req = self.system.create_parking_request("CAR-001", "ZONE-A")
        self.system.allocate_slot(req['request_id'])
        
        result = self.analytics.get_zone_metrics("ZONE-A")
        
        self.assertTrue(result['success'])
        self.assertEqual(result['zone_id'], "ZONE-A")
        self.assertEqual(result['total_requests'], 1)
        self.assertEqual(result['total_slots'], 10)
        
    def test_zone_metrics_nonexistent_zone(self):
        """Test zone metrics for non-existent zone"""
        result = self.analytics.get_zone_metrics("ZONE-X")
        self.assertFalse(result['success'])
        
    def test_average_parking_duration(self):
        """Test calculating average parking duration"""
        self.system.register_vehicle("CAR-001", VehicleType.CAR, "John Doe")
        req = self.system.create_parking_request("CAR-001", "ZONE-A")
        self.system.allocate_slot(req['request_id'])
        self.system.occupy_slot(req['request_id'])
        
        # Simulate parking for 2 hours
        request = self.system.requests[req['request_id']]
        request.entry_time = datetime.now() - timedelta(hours=2)
        
        self.system.release_slot(req['request_id'])
        
        result = self.analytics.get_overall_metrics()
        self.assertIsNotNone(result['average_parking_duration'])
        self.assertGreater(result['average_parking_duration'], 7000)  # ~2 hours in seconds
        
    def test_average_parking_duration_no_releases(self):
        """Test average parking duration with no releases"""
        self.system.register_vehicle("CAR-001", VehicleType.CAR, "John Doe")
        req = self.system.create_parking_request("CAR-001", "ZONE-A")
        self.system.allocate_slot(req['request_id'])
        
        result = self.analytics.get_overall_metrics()
        self.assertIsNone(result['average_parking_duration'])
        
    def test_generate_summary_report(self):
        """Test generating summary report"""
        self.system.register_vehicle("CAR-001", VehicleType.CAR, "John Doe")
        req = self.system.create_parking_request("CAR-001", "ZONE-A")
        self.system.allocate_slot(req['request_id'])
        
        result = self.analytics.generate_summary_report()
        
        self.assertTrue(result['success'])
        self.assertIn('summary', result)
        self.assertIsInstance(result['summary'], str)
        
    def test_peak_usage_tracking(self):
        """Test tracking peak usage"""
        # Create multiple requests and occupy slots
        for i in range(5):
            vehicle_id = f"CAR-{i:03d}"
            self.system.register_vehicle(vehicle_id, VehicleType.CAR, f"Owner {i}")
            req = self.system.create_parking_request(vehicle_id, "ZONE-A")
            self.system.allocate_slot(req['request_id'])
            self.system.occupy_slot(req['request_id'])
            
        result = self.analytics.get_overall_metrics()
        self.assertEqual(result['occupied_requests'], 5)
        
    def test_multiple_zones_metrics(self):
        """Test metrics across multiple zones"""
        self.system.add_zone("ZONE-B", "Zone B")
        self.system.add_parking_area("ZONE-B", "AREA-1", 5)
        
        self.system.register_vehicle("CAR-001", VehicleType.CAR, "John Doe")
        self.system.register_vehicle("CAR-002", VehicleType.CAR, "Jane Doe")
        
        req1 = self.system.create_parking_request("CAR-001", "ZONE-A")
        self.system.allocate_slot(req1['request_id'])
        
        req2 = self.system.create_parking_request("CAR-002", "ZONE-B")
        self.system.allocate_slot(req2['request_id'])
        
        result = self.analytics.get_overall_metrics()
        self.assertEqual(result['total_requests'], 2)
        self.assertEqual(result['total_slots'], 15)
        
    def test_export_analytics_to_file(self):
        """Test exporting analytics to file"""
        self.system.register_vehicle("CAR-001", VehicleType.CAR, "John Doe")
        req = self.system.create_parking_request("CAR-001", "ZONE-A")
        self.system.allocate_slot(req['request_id'])
        
        result = self.analytics.export_to_file()
        
        self.assertTrue(result['success'])
        self.assertIn('filepath', result)
        
        # Check file exists
        import os
        self.assertTrue(os.path.exists(result['filepath']))
        
    def test_penalty_statistics(self):
        """Test tracking allocation penalties"""
        self.system.add_zone("ZONE-B", "Zone B")
        self.system.link_adjacent_zones("ZONE-A", "ZONE-B")
        self.system.add_parking_area("ZONE-B", "AREA-1", 10)
        
        # Fill ZONE-A
        for i in range(10):
            vehicle_id = f"CAR-{i:03d}"
            self.system.register_vehicle(vehicle_id, VehicleType.CAR, f"Owner {i}")
            req = self.system.create_parking_request(vehicle_id, "ZONE-A")
            self.system.allocate_slot(req['request_id'])
            
        # Request ZONE-A but get ZONE-B with penalty
        self.system.register_vehicle("CAR-010", VehicleType.CAR, "Owner 10")
        req = self.system.create_parking_request("CAR-010", "ZONE-A")
        alloc = self.system.allocate_slot(req['request_id'])
        
        self.assertEqual(alloc['penalty'], 50)
        
    def test_cancellation_rate(self):
        """Test calculating cancellation rate"""
        self.system.register_vehicle("CAR-001", VehicleType.CAR, "John Doe")
        self.system.register_vehicle("CAR-002", VehicleType.CAR, "Jane Doe")
        self.system.register_vehicle("CAR-003", VehicleType.CAR, "Bob Smith")
        
        req1 = self.system.create_parking_request("CAR-001", "ZONE-A")
        self.system.allocate_slot(req1['request_id'])
        
        req2 = self.system.create_parking_request("CAR-002", "ZONE-A")
        self.system.cancel_request(req2['request_id'])
        
        req3 = self.system.create_parking_request("CAR-003", "ZONE-A")
        self.system.cancel_request(req3['request_id'])
        
        result = self.analytics.get_overall_metrics()
        # 2 out of 3 cancelled = ~66.67%
        self.assertEqual(result['cancelled_requests'], 2)
        self.assertEqual(result['total_requests'], 3)


if __name__ == '__main__':
    unittest.main()
