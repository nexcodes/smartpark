"""
ParkingSystem - Main controller that connects all components
"""
from zone import Zone
from vehicle import Vehicle
from parking_request import ParkingRequest
from allocation_engine import AllocationEngine
from rollback_manager import RollbackManager
from enums import RequestState


class ParkingSystem:
    """Main controller for the smart parking allocation system"""
    
    def __init__(self):
        """Initialize the parking system"""
        # Dictionary of zone_id -> Zone
        self.zones = {}
        
        # Dictionary of vehicle_id -> Vehicle
        self.vehicles = {}
        
        # Dictionary of request_id -> ParkingRequest
        self.requests = {}
        
        # Request counter for generating IDs
        self.request_counter = 0
        
        # Allocation engine
        self.allocation_engine = AllocationEngine(self.zones)
        
        # Rollback manager
        self.rollback_manager = RollbackManager()
        
        # History (linked list would be implemented here for DSA focus)
        # For simplicity, using Python list
        self.request_history = []
    
    def add_zone(self, zone_id):
        """
        Add a new zone to the system
        
        Args:
            zone_id: Unique identifier for the zone
            
        Returns:
            dict: Result with success status and message
        """
        if zone_id in self.zones:
            return {
                'success': False,
                'message': f'Zone {zone_id} already exists'
            }
        
        zone = Zone(zone_id)
        self.zones[zone_id] = zone
        return {
            'success': True,
            'message': f'Zone {zone_id} created successfully'
        }
    
    def add_parking_area_to_zone(self, zone_id, area_id, capacity):
        """
        Add a parking area to a specific zone
        
        Args:
            zone_id: ID of the zone
            area_id: ID for the parking area
            capacity: Number of parking slots
            
        Returns:
            dict: Result with success status and message
        """
        if zone_id not in self.zones:
            return {
                'success': False,
                'message': f'Zone {zone_id} not found'
            }
        
        self.zones[zone_id].add_parking_area(area_id, capacity)
        return {
            'success': True,
            'message': f'Parking area {area_id} added to {zone_id} with {capacity} slots'
        }
    
    def link_adjacent_zones(self, zone1_id, zone2_id):
        """
        Create bidirectional adjacency between two zones
        
        Args:
            zone1_id: First zone ID
            zone2_id: Second zone ID
            
        Returns:
            dict: Result with success status and message
        """
        if zone1_id not in self.zones or zone2_id not in self.zones:
            return {
                'success': False,
                'message': 'One or both zones not found'
            }
        
        self.zones[zone1_id].add_adjacent_zone(zone2_id)
        self.zones[zone2_id].add_adjacent_zone(zone1_id)
        return {
            'success': True,
            'message': f'Linked {zone1_id} ↔ {zone2_id}'
        }
    
    def register_vehicle(self, vehicle_id, preferred_zone):
        """
        Register a new vehicle in the system
        
        Args:
            vehicle_id: Unique identifier for the vehicle
            preferred_zone: Zone ID where vehicle prefers to park
            
        Returns:
            dict: Result with success status and message
        """
        if vehicle_id in self.vehicles:
            return {
                'success': False,
                'message': f'Vehicle {vehicle_id} already registered'
            }
        
        vehicle = Vehicle(vehicle_id, preferred_zone)
        self.vehicles[vehicle_id] = vehicle
        pref_msg = f' with preferred zone {preferred_zone}' if preferred_zone else ''
        return {
            'success': True,
            'message': f'Vehicle {vehicle_id} registered{pref_msg}'
        }
    
    def create_parking_request(self, vehicle_id, requested_zone):
        """
        Create a new parking request
        
        Args:
            vehicle_id: ID of the vehicle requesting parking
            requested_zone: Zone where parking is requested
            
        Returns:
            dict: Result with request_id and status
        """
        # Generate request ID
        self.request_counter += 1
        request_id = f"REQ{self.request_counter:04d}"
        
        # Create request
        request = ParkingRequest(request_id, vehicle_id, requested_zone)
        self.requests[request_id] = request
        self.request_history.append(request)
        
        return {
            'success': True,
            'request_id': request_id,
            'state': request.current_state.value,
            'message': f'Parking request {request_id} created'
        }
    
    def allocate_parking(self, request_id):
        """
        Allocate parking for a request
        
        Args:
            request_id: ID of the parking request
            
        Returns:
            dict: Allocation result
        """
        if request_id not in self.requests:
            return {
                'success': False,
                'message': 'Request not found'
            }
        
        request = self.requests[request_id]
        
        # Use allocation engine to allocate
        result = self.allocation_engine.allocate_slot(request)
        
        # If successful, record in rollback manager
        if result['success']:
            slot = self._find_slot(result['slot_id'])
            if slot:
                self.rollback_manager.record_allocation(slot, request)
        
        return result
    
    def cancel_parking_request(self, request_id):
        """
        Cancel a parking request
        
        Args:
            request_id: ID of the parking request
            
        Returns:
            dict: Cancellation result
        """
        if request_id not in self.requests:
            return {
                'success': False,
                'message': 'Request not found'
            }
        
        request = self.requests[request_id]
        previous_state = request.current_state
        
        # Use allocation engine to cancel
        result = self.allocation_engine.cancel_request(request)
        
        # If successful, record in rollback manager
        if result['success']:
            slot = None
            if request.allocated_slot_id:
                slot = self._find_slot(request.allocated_slot_id)
            self.rollback_manager.record_cancellation(slot, request, previous_state)
        
        return result
    
    def mark_parking_occupied(self, request_id):
        """
        Mark parking as occupied (vehicle has arrived)
        
        Args:
            request_id: ID of the parking request
            
        Returns:
            dict: Result
        """
        if request_id not in self.requests:
            return {
                'success': False,
                'message': 'Request not found'
            }
        
        request = self.requests[request_id]
        
        if request.change_state(RequestState.OCCUPIED):
            return {
                'success': True,
                'message': 'Parking marked as occupied'
            }
        else:
            return {
                'success': False,
                'message': f'Cannot mark as occupied from {request.current_state.value} state'
            }
    
    def release_parking(self, request_id):
        """
        Release parking (vehicle leaving)
        
        Args:
            request_id: ID of the parking request
            
        Returns:
            dict: Release result
        """
        if request_id not in self.requests:
            return {
                'success': False,
                'message': 'Request not found'
            }
        
        request = self.requests[request_id]
        
        # Use allocation engine to release
        result = self.allocation_engine.release_parking(request)
        
        # If successful, record in rollback manager
        if result['success']:
            slot = self._find_slot(request.allocated_slot_id)
            if slot:
                self.rollback_manager.record_release(slot, request)
        
        return result
    
    def rollback_operations(self, k):
        """
        Rollback the last k operations
        
        Args:
            k: Number of operations to rollback
            
        Returns:
            dict: Rollback result
        """
        return self.rollback_manager.rollback(k, self.zones, self.requests)
    
    def get_system_status(self):
        """
        Get overall system status
        
        Returns:
            dict: System statistics
        """
        total_slots = 0
        available_slots = 0
        
        for zone in self.zones.values():
            total_slots += zone.get_total_capacity()
            available_slots += zone.get_available_count()
        
        active_requests = 0
        for request in self.requests.values():
            if request.current_state in [RequestState.REQUESTED, RequestState.ALLOCATED, RequestState.OCCUPIED]:
                active_requests += 1
        
        return {
            'total_slots': total_slots,
            'available_slots': available_slots,
            'occupied_slots': total_slots - available_slots,
            'total_zones': len(self.zones),
            'total_requests': len(self.requests),
            'active_requests': active_requests,
            'operations_in_history': self.rollback_manager.get_operation_count()
        }
    
    def get_zone_status(self, zone_id):
        """
        Get status of a specific zone
        
        Args:
            zone_id: ID of the zone
            
        Returns:
            dict: Zone statistics or None if not found
        """
        if zone_id not in self.zones:
            return None
        
        zone = self.zones[zone_id]
        return {
            'zone_id': zone_id,
            'total_capacity': zone.get_total_capacity(),
            'available': zone.get_available_count(),
            'occupied': zone.get_occupied_count(),
            'areas': len(zone.parking_areas),
            'adjacent_zones': zone.adjacent_zones
        }
    
    def get_all_requests(self):
        """Get all parking requests"""
        return list(self.requests.values())
    
    def get_request_by_id(self, request_id):
        """Get a specific request by ID"""
        return self.requests.get(request_id)
    
    def _find_slot(self, slot_id):
        """Find a slot by its ID"""
        for zone in self.zones.values():
            for area in zone.parking_areas:
                for slot in area.slots:
                    if slot.slot_id == slot_id:
                        return slot
        return None
