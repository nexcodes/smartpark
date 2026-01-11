"""
Smart Parking Allocation & Management System
Main demonstration file showing system usage
"""
from parking_system import ParkingSystem
from enums import RequestState


def print_separator():
    """Print a visual separator"""
    print("\n" + "="*70 + "\n")


def demo_basic_operations():
    """Demonstrate basic parking operations"""
    print("=== SMART PARKING SYSTEM DEMO ===")
    print_separator()
    
    # Initialize the system
    system = ParkingSystem()
    print("✓ Parking system initialized")
    
    # Create zones
    print("\n--- Setting up zones ---")
    system.add_zone("ZONE-A")
    system.add_zone("ZONE-B")
    system.add_zone("ZONE-C")
    print("✓ Created zones: ZONE-A, ZONE-B, ZONE-C")
    
    # Add parking areas to zones
    print("\n--- Setting up parking areas ---")
    system.add_parking_area_to_zone("ZONE-A", "A1", 5)
    system.add_parking_area_to_zone("ZONE-A", "A2", 5)
    system.add_parking_area_to_zone("ZONE-B", "B1", 8)
    system.add_parking_area_to_zone("ZONE-C", "C1", 6)
    print("✓ ZONE-A: 2 areas (10 total slots)")
    print("✓ ZONE-B: 1 area (8 total slots)")
    print("✓ ZONE-C: 1 area (6 total slots)")
    
    # Link adjacent zones
    print("\n--- Linking adjacent zones ---")
    system.link_adjacent_zones("ZONE-A", "ZONE-B")
    system.link_adjacent_zones("ZONE-B", "ZONE-C")
    print("✓ ZONE-A ↔ ZONE-B")
    print("✓ ZONE-B ↔ ZONE-C")
    
    # Register vehicles
    print("\n--- Registering vehicles ---")
    system.register_vehicle("CAR-001", "ZONE-A")
    system.register_vehicle("CAR-002", "ZONE-A")
    system.register_vehicle("CAR-003", "ZONE-B")
    print("✓ Registered 3 vehicles")
    
    print_separator()
    
    # Test Case 1: Same-zone allocation
    print("TEST CASE 1: Same-zone allocation")
    print("-" * 40)
    result = system.create_parking_request("CAR-001", "ZONE-A")
    print(f"Created request: {result['request_id']}")
    
    alloc_result = system.allocate_parking(result['request_id'])
    if alloc_result['success']:
        print(f"✓ Allocated: {alloc_result['slot_id']} in {alloc_result['zone_id']}")
        print(f"  Penalty: {alloc_result['penalty']}")
        print(f"  Message: {alloc_result['message']}")
    
    print_separator()
    
    # Test Case 2: Cross-zone allocation (adjacent)
    print("TEST CASE 2: Cross-zone allocation to adjacent zone")
    print("-" * 40)
    
    # Fill up ZONE-A first
    print("Filling up ZONE-A...")
    for i in range(10):
        req_result = system.create_parking_request(f"FILL-{i}", "ZONE-A")
        system.allocate_parking(req_result['request_id'])
    
    zone_status = system.get_zone_status("ZONE-A")
    print(f"ZONE-A status: {zone_status['occupied']}/{zone_status['total_capacity']} occupied")
    
    # Now try to allocate in ZONE-A (should go to adjacent ZONE-B)
    result = system.create_parking_request("CAR-002", "ZONE-A")
    print(f"\nCreated request: {result['request_id']} for ZONE-A")
    
    alloc_result = system.allocate_parking(result['request_id'])
    if alloc_result['success']:
        print(f"✓ Allocated: {alloc_result['slot_id']} in {alloc_result['zone_id']}")
        print(f"  Penalty: {alloc_result['penalty']} (adjacent zone penalty)")
        print(f"  Message: {alloc_result['message']}")
    
    print_separator()
    
    # Test Case 3: Cancellation
    print("TEST CASE 3: Request cancellation")
    print("-" * 40)
    
    result = system.create_parking_request("CAR-003", "ZONE-B")
    request_id = result['request_id']
    print(f"Created request: {request_id}")
    
    alloc_result = system.allocate_parking(request_id)
    print(f"Allocated: {alloc_result['slot_id']}")
    
    # Cancel the request
    cancel_result = system.cancel_parking_request(request_id)
    print(f"\n✓ Cancelled: {cancel_result['message']}")
    
    request = system.get_request_by_id(request_id)
    print(f"  Request state: {request.current_state.value}")
    
    print_separator()
    
    # Test Case 4: Full parking lifecycle
    print("TEST CASE 4: Full parking lifecycle")
    print("-" * 40)
    
    result = system.create_parking_request("CAR-003", "ZONE-C")
    request_id = result['request_id']
    request = system.get_request_by_id(request_id)
    
    print(f"1. Created: {request_id} - State: {request.current_state.value}")
    
    alloc_result = system.allocate_parking(request_id)
    print(f"2. Allocated: {alloc_result['slot_id']} - State: {request.current_state.value}")
    
    system.mark_parking_occupied(request_id)
    print(f"3. Occupied: Vehicle arrived - State: {request.current_state.value}")
    
    system.release_parking(request_id)
    print(f"4. Released: Vehicle left - State: {request.current_state.value}")
    
    print_separator()
    
    # Test Case 5: Rollback operations
    print("TEST CASE 5: Rollback operations")
    print("-" * 40)
    
    print(f"Operations in history: {system.rollback_manager.get_operation_count()}")
    
    print("\nRolling back last 3 operations...")
    rollback_result = system.rollback_operations(3)
    
    if rollback_result['success']:
        print(f"✓ {rollback_result['message']}")
        for op in rollback_result['rolled_back']:
            print(f"  - Rolled back {op['operation']} on request {op['request_id']}")
    
    print_separator()
    
    # System status
    print("FINAL SYSTEM STATUS")
    print("-" * 40)
    status = system.get_system_status()
    print(f"Total slots: {status['total_slots']}")
    print(f"Available slots: {status['available_slots']}")
    print(f"Occupied slots: {status['occupied_slots']}")
    print(f"Total zones: {status['total_zones']}")
    print(f"Total requests: {status['total_requests']}")
    print(f"Active requests: {status['active_requests']}")
    
    print("\nZone Details:")
    for zone_id in ["ZONE-A", "ZONE-B", "ZONE-C"]:
        zone_status = system.get_zone_status(zone_id)
        print(f"  {zone_id}: {zone_status['available']}/{zone_status['total_capacity']} available")
    
    print_separator()


def demo_state_validation():
    """Demonstrate state machine validation"""
    print("=== STATE MACHINE VALIDATION DEMO ===")
    print_separator()
    
    system = ParkingSystem()
    system.add_zone("ZONE-A")
    system.add_parking_area_to_zone("ZONE-A", "A1", 5)
    
    # Create and allocate a request
    result = system.create_parking_request("TEST-CAR", "ZONE-A")
    request_id = result['request_id']
    system.allocate_parking(request_id)
    
    request = system.get_request_by_id(request_id)
    print(f"Current state: {request.current_state.value}")
    
    # Try invalid transition
    print("\nAttempting invalid transition (ALLOCATED -> RELEASED)...")
    success = request.change_state(RequestState.RELEASED)
    if not success:
        print("✓ Invalid transition correctly blocked!")
    
    # Valid transition
    print("\nAttempting valid transition (ALLOCATED -> OCCUPIED)...")
    success = request.change_state(RequestState.OCCUPIED)
    if success:
        print(f"✓ Valid transition successful! New state: {request.current_state.value}")
    
    print_separator()


if __name__ == "__main__":
    # Run basic operations demo
    demo_basic_operations()
    
    # Run state validation demo
    demo_state_validation()
    
    print("\n✓ All demonstrations completed successfully!")
    print("\nThe system is ready for UI integration (Phase 4)")
