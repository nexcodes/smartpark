"""
RollbackManager - handles rollback operations using stack data structure
"""
from enums import RequestState


class Operation:
    """Represents a single operation that can be rolled back"""
    
    def __init__(self, operation_type, slot_id, slot_previous_availability, 
                 slot_previous_vehicle_id, request_id, request_previous_state,
                 request_previous_allocated_slot=None, request_previous_allocated_zone=None):
        """
        Initialize an operation
        
        Args:
            operation_type: Type of operation (ALLOCATE, CANCEL, RELEASE)
            slot_id: ID of the affected slot
            slot_previous_availability: Previous availability state of the slot
            slot_previous_vehicle_id: Previous vehicle ID in the slot
            request_id: ID of the parking request
            request_previous_state: Previous state of the request
            request_previous_allocated_slot: Previous allocated slot ID
            request_previous_allocated_zone: Previous allocated zone ID
        """
        self.operation_type = operation_type
        self.slot_id = slot_id
        self.slot_previous_availability = slot_previous_availability
        self.slot_previous_vehicle_id = slot_previous_vehicle_id
        self.request_id = request_id
        self.request_previous_state = request_previous_state
        self.request_previous_allocated_slot = request_previous_allocated_slot
        self.request_previous_allocated_zone = request_previous_allocated_zone


class RollbackManager:
    """Manages rollback operations using a stack"""
    
    def __init__(self):
        """Initialize the rollback manager with an empty stack"""
        # Stack of Operation objects (using Python list as stack)
        self.operation_stack = []
    
    def record_allocation(self, slot, request):
        """
        Record an allocation operation for potential rollback
        
        Args:
            slot: ParkingSlot that was allocated
            request: ParkingRequest that was processed
        """
        operation = Operation(
            operation_type='ALLOCATE',
            slot_id=slot.slot_id,
            slot_previous_availability=True,  # Was available before allocation
            slot_previous_vehicle_id=None,
            request_id=request.request_id,
            request_previous_state=RequestState.REQUESTED,
            request_previous_allocated_slot=None,
            request_previous_allocated_zone=None
        )
        self.operation_stack.append(operation)
    
    def record_cancellation(self, slot, request, previous_state):
        """
        Record a cancellation operation for potential rollback
        
        Args:
            slot: ParkingSlot that was released (or None if not allocated)
            request: ParkingRequest that was cancelled
            previous_state: Previous state before cancellation
        """
        if slot:
            operation = Operation(
                operation_type='CANCEL',
                slot_id=slot.slot_id,
                slot_previous_availability=False,  # Was occupied before cancellation
                slot_previous_vehicle_id=request.vehicle_id,
                request_id=request.request_id,
                request_previous_state=previous_state,
                request_previous_allocated_slot=request.allocated_slot_id,
                request_previous_allocated_zone=request.allocated_zone
            )
        else:
            # Cancelled before allocation
            operation = Operation(
                operation_type='CANCEL',
                slot_id=None,
                slot_previous_availability=None,
                slot_previous_vehicle_id=None,
                request_id=request.request_id,
                request_previous_state=previous_state,
                request_previous_allocated_slot=None,
                request_previous_allocated_zone=None
            )
        self.operation_stack.append(operation)
    
    def record_release(self, slot, request):
        """
        Record a release operation for potential rollback
        
        Args:
            slot: ParkingSlot that was released
            request: ParkingRequest that was released
        """
        operation = Operation(
            operation_type='RELEASE',
            slot_id=slot.slot_id,
            slot_previous_availability=False,  # Was occupied before release
            slot_previous_vehicle_id=request.vehicle_id,
            request_id=request.request_id,
            request_previous_state=RequestState.OCCUPIED,
            request_previous_allocated_slot=request.allocated_slot_id,
            request_previous_allocated_zone=request.allocated_zone
        )
        self.operation_stack.append(operation)
    
    def rollback(self, k, zones, requests_dict):
        """
        Rollback the last k operations
        
        Args:
            k: Number of operations to rollback
            zones: Dictionary of zone_id -> Zone objects
            requests_dict: Dictionary of request_id -> ParkingRequest objects
            
        Returns:
            dict: Result with success status and list of rolled back operations
        """
        if k <= 0:
            return {
                'success': False,
                'message': 'k must be positive',
                'rolled_back': []
            }
        
        if k > len(self.operation_stack):
            return {
                'success': False,
                'message': f'Cannot rollback {k} operations - only {len(self.operation_stack)} in history',
                'rolled_back': []
            }
        
        rolled_back = []
        skipped = []
        
        for _ in range(k):
            if not self.operation_stack:
                break
            
            # Pop operation from stack
            operation = self.operation_stack.pop()
            
            # Get the request
            request = requests_dict.get(operation.request_id)
            if not request:
                skipped.append(operation.request_id)
                continue
            
            # Rollback based on operation type
            if operation.operation_type == 'ALLOCATE':
                self._rollback_allocation(operation, zones, request)
            elif operation.operation_type == 'CANCEL':
                self._rollback_cancellation(operation, zones, request)
            elif operation.operation_type == 'RELEASE':
                self._rollback_release(operation, zones, request)
            
            rolled_back.append({
                'operation': operation.operation_type,
                'request_id': operation.request_id,
                'slot_id': operation.slot_id
            })
        
        return {
            'success': True,
            'message': f'Successfully rolled back {len(rolled_back)} operations',
            'rolled_back': rolled_back,
            'skipped': skipped
        }
    
    def _rollback_allocation(self, operation, zones, request):
        """Rollback an allocation operation"""
        # Find and release the slot
        slot = self._find_slot(operation.slot_id, zones)
        if slot:
            slot.is_available = operation.slot_previous_availability
            slot.occupied_vehicle_id = operation.slot_previous_vehicle_id
        
        # Restore request state
        request.current_state = operation.request_previous_state
        request.allocated_slot_id = operation.request_previous_allocated_slot
        request.allocated_zone = operation.request_previous_allocated_zone
        request.allocation_timestamp = None
    
    def _rollback_cancellation(self, operation, zones, request):
        """Rollback a cancellation operation"""
        # Restore slot if it was allocated
        if operation.slot_id:
            slot = self._find_slot(operation.slot_id, zones)
            if slot:
                slot.is_available = operation.slot_previous_availability
                slot.occupied_vehicle_id = operation.slot_previous_vehicle_id
        
        # Restore request state
        request.current_state = operation.request_previous_state
        request.allocated_slot_id = operation.request_previous_allocated_slot
        request.allocated_zone = operation.request_previous_allocated_zone
    
    def _rollback_release(self, operation, zones, request):
        """Rollback a release operation"""
        # Find and re-occupy the slot
        slot = self._find_slot(operation.slot_id, zones)
        if slot:
            slot.is_available = operation.slot_previous_availability
            slot.occupied_vehicle_id = operation.slot_previous_vehicle_id
        
        # Restore request state
        request.current_state = operation.request_previous_state
        request.release_timestamp = None
    
    def _find_slot(self, slot_id, zones):
        """Find a slot by its ID"""
        for zone in zones.values():
            for area in zone.parking_areas:
                for slot in area.slots:
                    if slot.slot_id == slot_id:
                        return slot
        return None
    
    def get_operation_count(self):
        """Get the number of operations in the stack"""
        return len(self.operation_stack)
