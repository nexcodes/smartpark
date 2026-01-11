"""
Smart Parking Allocation & Management System
Interactive user-controlled interface
"""
from parking_system import ParkingSystem


def print_separator():
    """Print a visual separator"""
    print("\n" + "="*70 + "\n")


def print_menu():
    """Display the main menu"""
    print("\n" + "="*70)
    print("        SMART PARKING ALLOCATION & MANAGEMENT SYSTEM")
    print("="*70)
    print("\n--- SETUP OPERATIONS ---")
    print("1.  Add Zone")
    print("2.  Add Parking Area to Zone")
    print("3.  Link Adjacent Zones")
    print("4.  Register Vehicle")
    
    print("\n--- PARKING OPERATIONS ---")
    print("5.  Create Parking Request")
    print("6.  Allocate Parking")
    print("7.  Mark Parking as Occupied")
    print("8.  Release Parking")
    print("9.  Cancel Parking Request")
    
    print("\n--- QUERY OPERATIONS ---")
    print("10. View System Status")
    print("11. View Zone Status")
    print("12. View Request Details")
    print("13. View All Zones")
    print("14. View All Vehicles")
    
    print("\n--- ANALYTICS ---")
    print("17. View Comprehensive Analytics")
    print("18. View Average Parking Duration")
    print("19. View Zone Utilization")
    print("20. View Request Statistics")
    print("21. View Peak Usage Zone")
    print("22. View Cross-Zone Statistics")
    
    print("\n--- ADVANCED OPERATIONS ---")
    print("15. Rollback Operations")
    print("16. View Operation History")
    
    print("\n--- SYSTEM ---")
    print("0.  Exit")
    print("="*70)


def add_zone(system):
    """Add a new zone"""
    zone_id = input("Enter Zone ID (e.g., ZONE-A): ").strip().upper()
    if not zone_id:
        print("❌ Zone ID cannot be empty!")
        return
    
    result = system.add_zone(zone_id)
    if result['success']:
        print(f"✓ {result['message']}")
    else:
        print(f"❌ {result['message']}")


def add_parking_area(system):
    """Add parking area to a zone"""
    zone_id = input("Enter Zone ID: ").strip().upper()
    area_id = input("Enter Area ID (e.g., A1): ").strip().upper()
    try:
        capacity = int(input("Enter capacity (number of slots): "))
        if capacity <= 0:
            print("❌ Capacity must be positive!")
            return
    except ValueError:
        print("❌ Invalid capacity! Please enter a number.")
        return
    
    result = system.add_parking_area_to_zone(zone_id, area_id, capacity)
    if result['success']:
        print(f"✓ {result['message']}")
    else:
        print(f"❌ {result['message']}")


def link_zones(system):
    """Link two adjacent zones"""
    zone1 = input("Enter first Zone ID: ").strip().upper()
    zone2 = input("Enter second Zone ID: ").strip().upper()
    
    result = system.link_adjacent_zones(zone1, zone2)
    if result['success']:
        print(f"✓ {result['message']}")
    else:
        print(f"❌ {result['message']}")


def register_vehicle(system):
    """Register a new vehicle"""
    vehicle_id = input("Enter Vehicle ID (e.g., CAR-001): ").strip().upper()
    preferred_zone = input("Enter preferred zone (optional, press Enter to skip): ").strip().upper()
    
    if not preferred_zone:
        preferred_zone = None
    
    result = system.register_vehicle(vehicle_id, preferred_zone)
    if result['success']:
        print(f"✓ {result['message']}")
    else:
        print(f"❌ {result['message']}")


def create_parking_request(system):
    """Create a new parking request"""
    vehicle_id = input("Enter Vehicle ID: ").strip().upper()
    requested_zone = input("Enter requested zone: ").strip().upper()
    
    result = system.create_parking_request(vehicle_id, requested_zone)
    if result['success']:
        print(f"✓ {result['message']}")
        print(f"  Request ID: {result['request_id']}")
        print(f"  State: {result['state']}")
    else:
        print(f"❌ {result['message']}")


def allocate_parking(system):
    """Allocate parking for a request"""
    request_id = input("Enter Request ID: ").strip()
    
    result = system.allocate_parking(request_id)
    if result['success']:
        print(f"✓ {result['message']}")
        print(f"  Slot: {result['slot_id']}")
        print(f"  Zone: {result['zone_id']}")
        print(f"  Penalty: {result['penalty']}")
    else:
        print(f"❌ {result['message']}")


def mark_occupied(system):
    """Mark parking as occupied"""
    request_id = input("Enter Request ID: ").strip()
    
    result = system.mark_parking_occupied(request_id)
    if result['success']:
        print(f"✓ {result['message']}")
    else:
        print(f"❌ {result['message']}")


def release_parking(system):
    """Release parking slot"""
    request_id = input("Enter Request ID: ").strip()
    
    result = system.release_parking(request_id)
    if result['success']:
        print(f"✓ {result['message']}")
    else:
        print(f"❌ {result['message']}")


def cancel_request(system):
    """Cancel a parking request"""
    request_id = input("Enter Request ID: ").strip()
    
    result = system.cancel_parking_request(request_id)
    if result['success']:
        print(f"✓ {result['message']}")
    else:
        print(f"❌ {result['message']}")


def view_system_status(system):
    """Display system status"""
    print_separator()
    print("SYSTEM STATUS")
    print("-" * 40)
    status = system.get_system_status()
    print(f"Total slots:      {status['total_slots']}")
    print(f"Available slots:  {status['available_slots']}")
    print(f"Occupied slots:   {status['occupied_slots']}")
    print(f"Total zones:      {status['total_zones']}")
    print(f"Total requests:   {status['total_requests']}")
    print(f"Active requests:  {status['active_requests']}")
    print_separator()


def view_zone_status(system):
    """Display status of a specific zone"""
    zone_id = input("Enter Zone ID: ").strip().upper()
    
    try:
        status = system.get_zone_status(zone_id)
        if status is None:
            print(f"❌ Zone '{zone_id}' not found")
            return
        print_separator()
        print(f"ZONE STATUS: {zone_id}")
        print("-" * 40)
        print(f"Total capacity:   {status['total_capacity']}")
        print(f"Available slots:  {status['available']}")
        print(f"Occupied slots:   {status['occupied']}")
        print(f"Number of areas:  {status['areas']}")
        print(f"\nAdjacent zones:   {', '.join(status['adjacent_zones']) if status['adjacent_zones'] else 'None'}")
        print_separator()
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def view_request_details(system):
    """Display details of a parking request"""
    request_id = input("Enter Request ID: ").strip()
    
    try:
        request = system.get_request_by_id(request_id)
        if request:
            print_separator()
            print(f"REQUEST DETAILS: {request_id}")
            print("-" * 40)
            print(f"Vehicle ID:       {request.vehicle_id}")
            print(f"Requested Zone:   {request.requested_zone}")
            print(f"Current State:    {request.current_state.value}")
            print(f"Created At:       {request.timestamp}")
            if request.allocated_slot_id:
                print(f"Allocated Slot:   {request.allocated_slot_id}")
                print(f"Allocated Zone:   {request.allocated_zone}")
            print_separator()
        else:
            print(f"❌ Request {request_id} not found!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def view_all_zones(system):
    """Display all zones in the system"""
    print_separator()
    print("ALL ZONES")
    print("-" * 40)
    status = system.get_system_status()
    if status['total_zones'] == 0:
        print("No zones created yet.")
    else:
        for zone_id in system.zones:
            zone_status = system.get_zone_status(zone_id)
            print(f"{zone_id}: {zone_status['available']}/{zone_status['total_capacity']} available")
    print_separator()


def view_all_vehicles(system):
    """Display all registered vehicles"""
    print_separator()
    print("ALL VEHICLES")
    print("-" * 40)
    if not system.vehicles:
        print("No vehicles registered yet.")
    else:
        for vehicle_id, vehicle in system.vehicles.items():
            pref_zone = vehicle.preferred_zone if vehicle.preferred_zone else "None"
            print(f"{vehicle_id} - Preferred Zone: {pref_zone}")
    print_separator()


def rollback_operations(system):
    """Rollback recent operations"""
    try:
        count = int(input("Enter number of operations to rollback: "))
        if count <= 0:
            print("❌ Count must be positive!")
            return
        
        result = system.rollback_operations(count)
        if result['success']:
            print(f"✓ {result['message']}")
            if result['rolled_back']:
                print("\nRolled back operations:")
                for op in result['rolled_back']:
                    print(f"  - {op['operation']} on request {op['request_id']}")
        else:
            print(f"❌ {result['message']}")
    except ValueError:
        print("❌ Invalid count! Please enter a number.")


def view_operation_history(system):
    """Display operation history"""
    print_separator()
    print("OPERATION HISTORY")
    print("-" * 40)
    count = system.rollback_manager.get_operation_count()
    print(f"Total operations in history: {count}")
    print_separator()


def view_comprehensive_analytics(system):
    """Display comprehensive analytics summary"""
    print_separator()
    summary = system.analytics.display_analytics_summary()
    print(summary)


def view_average_duration(system):
    """Display average parking duration"""
    print_separator()
    print("AVERAGE PARKING DURATION")
    print("-" * 40)
    result = system.analytics.get_average_parking_duration()
    
    if result['completed_requests'] > 0:
        print(f"Average Duration: {result['average_duration_minutes']} minutes")
        print(f"                 ({result['average_duration_seconds']} seconds)")
        print(f"Completed Sessions: {result['completed_requests']}")
    else:
        print(result['message'])
    print_separator()


def view_zone_utilization(system):
    """Display zone utilization rates"""
    print_separator()
    print("ZONE UTILIZATION RATES")
    print("-" * 40)
    result = system.analytics.get_zone_utilization()
    
    if result['success'] and result['zones']:
        for zone in result['zones']:
            print(f"{zone['zone_id']}:")
            print(f"  Utilization: {zone['utilization_rate']}%")
            print(f"  Occupied: {zone['occupied']}/{zone['total_capacity']}")
            print(f"  Available: {zone['available']}")
            print()
    else:
        print(result.get('message', 'No data available'))
    print_separator()


def view_request_statistics(system):
    """Display request statistics"""
    print_separator()
    print("REQUEST STATISTICS")
    print("-" * 40)
    result = system.analytics.get_request_statistics()
    
    print(f"Total Requests: {result['total_requests']}")
    print(f"\nState Breakdown:")
    print(f"  Requested: {result['state_breakdown']['requested']}")
    print(f"  Allocated: {result['state_breakdown']['allocated']}")
    print(f"  Occupied: {result['state_breakdown']['occupied']}")
    print(f"  Released: {result['state_breakdown']['released']}")
    print(f"  Cancelled: {result['state_breakdown']['cancelled']}")
    print(f"\nCompletion Rate: {result['completion_rate']}%")
    print(f"Cancellation Rate: {result['cancellation_rate']}%")
    print_separator()


def view_peak_usage_zone(system):
    """Display peak usage zone"""
    print_separator()
    print("PEAK USAGE ZONE")
    print("-" * 40)
    result = system.analytics.get_peak_usage_zone()
    
    if result['success']:
        print(f"Zone: {result['zone_id']}")
        print(f"Utilization: {result['utilization_rate']}%")
        print(f"Occupied: {result['occupied']}/{result['total_capacity']}")
        print(f"Available: {result['available']}")
    else:
        print(result['message'])
    print_separator()


def view_cross_zone_statistics(system):
    """Display cross-zone allocation statistics"""
    print_separator()
    print("CROSS-ZONE ALLOCATION STATISTICS")
    print("-" * 40)
    result = system.analytics.get_cross_zone_allocation_statistics()
    
    print(f"Total Allocations: {result['total_allocated']}")
    print(f"Same Zone: {result['same_zone_allocations']}")
    print(f"Cross Zone: {result['cross_zone_allocations']}")
    print(f"Cross-Zone Percentage: {result['cross_zone_percentage']}%")
    print_separator()


def main():
    """Main application loop"""
    print("\n🚗 Initializing Smart Parking System...")
    system = ParkingSystem()
    print("✓ System initialized successfully!\n")
    
    while True:
        print_menu()
        choice = input("\nEnter your choice: ").strip()
        
        try:
            if choice == "0":
                print("\n👋 Thank you for using Smart Parking System!")
                break
            elif choice == "1":
                add_zone(system)
            elif choice == "2":
                add_parking_area(system)
            elif choice == "3":
                link_zones(system)
            elif choice == "4":
                register_vehicle(system)
            elif choice == "5":
                create_parking_request(system)
            elif choice == "6":
                allocate_parking(system)
            elif choice == "7":
                mark_occupied(system)
            elif choice == "8":
                release_parking(system)
            elif choice == "9":
                cancel_request(system)
            elif choice == "10":
                view_system_status(system)
            elif choice == "11":
                view_zone_status(system)
            elif choice == "12":
                view_request_details(system)
            elif choice == "13":
                view_all_zones(system)
            elif choice == "14":
                view_all_vehicles(system)
            elif choice == "15":
                rollback_operations(system)
            elif choice == "16":
                view_operation_history(system)
            elif choice == "17":
                view_comprehensive_analytics(system)
            elif choice == "18":
                view_average_duration(system)
            elif choice == "19":
                view_zone_utilization(system)
            elif choice == "20":
                view_request_statistics(system)
            elif choice == "21":
                view_peak_usage_zone(system)
            elif choice == "22":
                view_cross_zone_statistics(system)
            else:
                print("❌ Invalid choice! Please select a valid option.")
        except Exception as e:
            print(f"❌ An error occurred: {str(e)}")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
